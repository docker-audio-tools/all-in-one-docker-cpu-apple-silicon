docker run -it \
   -v $PWD/audio:/app/input \
   -v $PWD/results:/app/output \
   allinone \
   --out-dir /app/output/analysis \
   /app/input/japonesa.wav
