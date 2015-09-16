export DISPLAY=":0"
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
IMGA=/dev/shm/first.png
IMGB=/dev/shm/second.png

while :
do
   #grab a couple images with a slightly randomized time between them
   sleep $(( ( RANDOM % 10 ) + 5 ))
   nice -n 19 scrot ${IMGA}
   sleep $(( ( RANDOM % 10 ) + 5 ))
   nice -n 19 scrot ${IMGB}

   #crop and adjust images
   nice -n 19 convert ${IMGA} -gravity center -crop 100x5%+0+0 -solarize 80% -colorspace Gray ${IMGA}
   nice -n 19 convert ${IMGB} -gravity center -crop 100x5%+0+0 -solarize 80% -colorspace Gray ${IMGB}
   
   #compare the images
   IMGASTD=$(
      nice -n 19 identify -verbose -alpha off ${IMGA}              \
        | sed -n '/Histogram/q; /Colormap/q; /statistics:/,$ p'    \
        | grep 'standard deviation:'                               \
        | awk '{ print $3; }'
   )

   IMGBSTD=$(
      nice -n 19 identify -verbose -alpha off ${IMGB}              \
        | sed -n '/Histogram/q; /Colormap/q; /statistics:/,$ p'    \
        | grep 'standard deviation:'                               \
        | awk '{ print $3; }'
   )

   DIFF=$( cat <<EOD |
define abs(i) {
  if (i < 0) return (-i)
  return (i)
}
abs(${IMGASTD} - ${IMGBSTD}) < 0.2
quit
EOD
   bc )

   #determine if they were pretty close to the same image
   if [[ $DIFF -eq 1 ]]
   then
      WID=$(xdotool search --onlyvisible --class chromium|head -1)
      xdotool windowactivate ${WID}
      xdotool key Home
      sleep 1
      xdotool key ctrl+F5
   fi
done
