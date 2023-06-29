# Crestron NVX Autoloader
A python tool for discovering, updating, and configuring multiple Crestron NVX encoders/decoders in parallel

## Motivation
Company needed to prepare over 900 Crestron NVX encoders/decoders for installation. Each device needed updated firmware, and unique and predetermined hostname,
ip address, subnet mask, and default gateway. Individually, completing this for a single device (including unpacking and repacking) takes about 30 minutes. Company sought a faster way to complete this task.

## Results
With this tool, 16 devices were simulatenously unpacked, connected, discovered, updated, configured, and repacked within 40 minutes. Total time per device reduced from 30 minutes to 2.5 minutes, saving over 412 man-hours.

## Process
1. Crestron discovery packet is sent on broadcast address. 
2. All connected NVX device IP addresses become known.
3. SSH into each IP address to intialize device
4. Update firmware, if needed, using sftp
5. Use WebSocket to access Crestron web-based device interface
6. Find device MAC address within CSV, gather information to be uploaded
7. Upload network info through WebSocket and restart
8. Print IP and Hostname through label-printer, control light on device to identify

