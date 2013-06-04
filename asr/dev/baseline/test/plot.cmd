set xlabel "number of templetes"
set ylabel "recognition accuracy(%)"
set title "no.templetes vs accuracy"
plot "res_novad.txt" u 1:2 w lp pt 2 title "novad", \
"res_vad.txt" u 1:2 w lp pt 2 title "vad" 
set xrange [1:100]
replot
