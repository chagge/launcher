package main

import (
	"encoding/binary"
	"os"
)

var BYTE_ORDER = binary.BigEndian

const RespondLimit int = 800
const Alpha int16 = 3

type HTKWav struct {
	NumSamp    uint32
	SampPeriod uint32
	SampSize   uint16
	SampKind   uint16
	Data       []int16
}

func ReadHTKWav(fd *os.File) *HTKWav {
	w := new(HTKWav)
	binary.Read(fd, BYTE_ORDER, &w.NumSamp)
	binary.Read(fd, BYTE_ORDER, &w.SampPeriod)
	binary.Read(fd, BYTE_ORDER, &w.SampSize)
	binary.Read(fd, BYTE_ORDER, &w.SampKind)
	w.Data = make([]int16, w.NumSamp)
	for i := 0; i < len(w.Data); i++ {
		binary.Read(fd, BYTE_ORDER, &w.Data[i])
	}
	return w
}

func WriteHTKWav(w *HTKWav, fd *os.File) {
	binary.Write(fd, BYTE_ORDER, w.NumSamp)
	binary.Write(fd, BYTE_ORDER, w.SampPeriod)
	binary.Write(fd, BYTE_ORDER, w.SampSize)
	binary.Write(fd, BYTE_ORDER, w.SampKind)
	for i := 0; i < len(w.Data); i++ {
		binary.Write(fd, BYTE_ORDER, w.Data[i])
	}
}

func (w *HTKWav) vad() {
	var start, end int
	var maxAbs int16 = 0
	for i := 0; i < RespondLimit; i++ {
		if w.Data[i] > maxAbs {
			maxAbs = w.Data[i]
		}
		if w.Data[i] < -maxAbs {
			maxAbs = -w.Data[i]
		}
	}
	thres := Alpha * maxAbs
	for i := 0; i < len(w.Data); i++ {
		if w.Data[i] > thres || w.Data[i] < -thres {
			start = i
			break
		}
	}
	for i := len(w.Data); i > 0; i-- {
		if w.Data[i-1] > thres || w.Data[i-1] < -thres {
			end = i
			break
		}
	}
	//println(len(w.Data) - (end-start))
	w.Data = w.Data[start:end]
	w.NumSamp = uint32(len(w.Data))
}

func main() {
	ifd, _ := os.Open(os.Args[1])
	defer ifd.Close()
	ofd, _ := os.Create(os.Args[2])
	defer ofd.Close()
	w := ReadHTKWav(ifd)
	w.vad()
	WriteHTKWav(w, ofd)
}
