set xlabel "number of templetes"
set ylabel "recognition accuracy(%)"
set title "no.templetes vs accuracy"
plot "EM1.txt" u 1:2 w lp pt 2 title "1", \
"EM2.txt" u 1:2 w lp pt 3 title "2"
set xrange [1:100]
replot
