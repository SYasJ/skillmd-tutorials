#!/usr/bin/env bash
# ep013 · skill.md · read-only check: which kernel is running, and is a newer one installed or pending?
# Changes nothing. Run:  bash check-kernel.sh
set -u
echo "Running kernel : $(uname -r)"
if command -v apt >/dev/null 2>&1; then
  echo "Distro family  : Debian / Ubuntu"
  echo "Newest installed linux-image packages:"
  dpkg -l 'linux-image-[0-9]*' 2>/dev/null | awk '/^ii/{print "  " $2 "  " $3}' | tail -3
  [ -f /var/run/reboot-required ] && echo "REBOOT REQUIRED: a new kernel or library is waiting (/var/run/reboot-required)"
  echo "To update:  sudo apt update && sudo apt full-upgrade   then   sudo reboot"
elif command -v dnf >/dev/null 2>&1; then
  echo "Distro family  : Fedora / RHEL"
  echo "Installed kernels (newest last):"
  rpm -q kernel 2>/dev/null | sort -V | tail -3 | sed 's/^/  /'
  command -v needs-restarting >/dev/null 2>&1 && { needs-restarting -r >/dev/null 2>&1 || echo "REBOOT REQUIRED (needs-restarting -r)"; }
  echo "To update:  sudo dnf upgrade --refresh   then   sudo reboot"
else
  echo "Unknown package manager: use your distro's update tool, then reboot."
fi
