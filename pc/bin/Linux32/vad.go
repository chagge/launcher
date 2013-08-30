package main

import (
	"encoding/binary"
	"fmt"
	"math"
	"os"
)

var (
	FileEndian         = binary.BigEndian
	Alpha      float64 = 3.5
	NumNearby  int     = 10
)

const (
	timeFrame_ns = 10 * 1e6  // 10ms presented in ns metric
	timeBG_ns    = 150 * 1e6 // begin 150ms are assumed to be pure BackGround Noise
)

type Wav struct {
	NumSample    int
	SamplePeriod int // in 100ns
	SampleSize   int
	SampleKind   int
	Samples      []int
}

func ReadWav(fname string) *Wav {
	fd, err := os.Open(fname)
	defer fd.Close()
	if err != nil {
		panic("ReadWav: Can't load specified file:" + fname)
	}

	var buf32 int32
	var buf16 int16
	w := new(Wav)

	binary.Read(fd, FileEndian, &buf32)
	w.NumSample = int(buf32)

	binary.Read(fd, FileEndian, &buf32)
	w.SamplePeriod = int(buf32)

	binary.Read(fd, FileEndian, &buf16)
	w.SampleSize = int(buf16)

	binary.Read(fd, FileEndian, &buf16)
	w.SampleKind = int(buf16)

	w.Samples = make([]int, w.NumSample)
	for i := 0; i < w.NumSample; i++ {
		binary.Read(fd, FileEndian, &buf16)
		w.Samples[i] = int(buf16)
	}
    fmt.Println(w.NumSample, w.SamplePeriod, w.SampleSize, w.SampleKind)
	return w
}

func WriteWav(w *Wav, fname string) {
	fd, err := os.Create(fname)
	defer fd.Close()
	if err != nil {
		panic("WriteWav: Can't create specified file:" + fname)
	}
	binary.Write(fd, FileEndian, int32(w.NumSample))
	binary.Write(fd, FileEndian, int32(w.SamplePeriod))
	binary.Write(fd, FileEndian, int16(w.SampleSize))
	binary.Write(fd, FileEndian, int16(w.SampleKind))
	for i := 0; i < w.NumSample; i++ {
		binary.Write(fd, FileEndian, int16(w.Samples[i]))
	}
}

func main() {
	ifname := os.Args[1]
	ofname := os.Args[2]
	w := ReadWav(ifname)
	var frameLen int = timeFrame_ns / (w.SamplePeriod * 100) // HTK use 100ns as basic time unit
	var numFrame int = w.NumSample / frameLen                // interger division rounds off the end fractional frame
    fmt.Println("numFrame", numFrame)
    fmt.Println("total Samples", w.NumSample)
	frameEs := make([]float64, numFrame)
	for i := 0; i < numFrame; i++ {
		s := w.Samples[i*frameLen : (i+1)*frameLen]
		// float64 is used to avoid overflow, but not guaranteed
		var frameE float64 = 0.0
		for k := 0; k < frameLen; k++ {
			frameE += (float64(s[k]) * float64(s[k]))
		}
		frameEs[i] = math.Log(frameE)
	}

	var sum1, sum2 float64 = 0.0, 0.0
	M := int(timeBG_ns / timeFrame_ns) // number of frames for BackGround estimation
    fmt.Println("M = ", M)
	for _, e := range frameEs[:M] {
		sum1 += e
		sum2 += e * e
	}
	eMean := sum1 / float64(M)
	eDelta := math.Sqrt(sum2/float64(M) - eMean*eMean)

	bgEBound := eMean + Alpha*eDelta

	// [begin, end) will cover voice activity
	begin, end := 0, numFrame
	// detect beginning frame, inclusive
	for i := 0; i+NumNearby <= numFrame; i++ {
		nearby := frameEs[i : i+NumNearby]
		VA := true
		for _, e := range nearby {
			if e < bgEBound {
				VA = false
			}
		}
		if VA {
			begin = i
			break
		}

	}

	// detect ending frame, exlusive
	for i := numFrame; i-NumNearby >= 0; i-- {
		nearby := frameEs[i-NumNearby : i]
		VA := true
		for _, e := range nearby {
			if e < bgEBound {
				VA = false
			}
		}
		if VA {
			end = i
			break
		}
	}
    fmt.Println(0, len(frameEs))
	fmt.Println(begin, end)
    //fmt.Println(frameEs)
	// chop
	w.Samples = w.Samples[begin*frameLen : end*frameLen]
	w.NumSample = len(w.Samples)
	WriteWav(w, ofname)
}
