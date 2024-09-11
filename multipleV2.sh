
base_port=5201

num_servers=$1
shift

report_base=$1
shift

iperf_options="$*"

for i in $(seq 1 $num_servers); do

    server_port=$(($base_port + $i))

    report_file=${report_base}-${server_port}.txt

    iperf3 -s -p $server_port $iperf_options &> $report_file &

    echo "Started iperf3 server on port $server_port, logging to $report_file"
done
