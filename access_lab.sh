sudo docker run -it -p 127.0.0.1:8003:8000 --user="$(id -u):$(id -g)" -v $(pwd):/lab felix11h/neuroenv_smt_ltx /bin/bash
