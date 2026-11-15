#!/bin/zsh
# The exact command sequence from the video (chrome-devtools-mcp v1.13.0, macOS, Nov 15 2026).
# Everything lives in /tmp/cdm-demo; nothing is installed globally.
set -e
mkdir -p /tmp/cdm-demo/site /tmp/cdm-demo/out && cd /tmp/cdm-demo
cp "$(dirname "$0")/demo-site/index-broken.html" site/index.html
npm view chrome-devtools-mcp version license scripts.postinstall scripts.install
npm i --prefix /tmp/cdm-demo chrome-devtools-mcp@1.13.0 --no-audit --no-fund
export PATH=/tmp/cdm-demo/node_modules/.bin:$PATH CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1
(cd site && python3 -m http.server 9744 --bind 127.0.0.1 >/dev/null 2>&1 &)
sleep 1
chrome-devtools start --no-usage-statistics --no-performance-crux --workspace=/tmp/cdm-demo/out
chrome-devtools navigate_page 1 --url http://127.0.0.1:9744/
chrome-devtools take_snapshot 1            # the Buy button was uid 1_3 in our run
chrome-devtools click 1 1_3
chrome-devtools list_console_messages 1    # -> Uncaught ReferenceError: cart is not defined
chrome-devtools list_network_requests 1    # -> logo.png [404], favicon.ico [404]
chrome-devtools take_screenshot 1 --filePath /tmp/cdm-demo/out/shop.png   # inside workspace: saved
chrome-devtools take_screenshot 1 --filePath /Users/Shared/shop.png || true  # outside: Access denied
chrome-devtools lighthouse_audit 1 --mode snapshot | head -14
chrome-devtools stop
echo "Now swap in demo-site/index-fixed.html (+ any logo.png), restart, TAKE A NEW SNAPSHOT, click again."
# Cleanup when done: pkill -f "http.server 9744"; rm -rf /tmp/cdm-demo
