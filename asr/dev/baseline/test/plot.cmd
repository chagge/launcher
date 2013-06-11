set xlabel "number of templetes"
set ylabel "recognition accuracy(%)"
set title "no.templetes vs accuracy"
plot "res_novad.txt" u 1:2 w lp pt 2 title "novad", \
"res_vad_alpha2.txt" u 1:2 w lp pt 2 title "vad2", \
"res_vad_alpha4.txt" u 1:2 w lp pt 2 title "vad4" 
set xrange [1:100]
replot
