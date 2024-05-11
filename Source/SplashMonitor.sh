#!/bin/bash
#------------------------------------------------------------------------------
# =========                 |
# \\      /  F ield         | Splash: Your Application Name
#  \\    /   O peration     |
#   \\  /    A nd           | www.simulitica.com
#    \\/     M anipulation  |
#-------------------------------------------------------------------------------
#    Copyright (C) [2023] Splash by Simulitica Ltd.
#------------------------------------------------------------------------------
# License
#     This file is part of Splash, distributed under a Proprietary License.
#
# Script
#     splashMonitor
#
# Description
#     Monitor data with Gnuplot for Splash application
#     - requires gnuplot
#
#------------------------------------------------------------------------------

printHelp() {
    cat<<USAGE

Usage: ${0##*/} [OPTIONS] <file>
Options:
  -g | -grid            Draw grid lines
  -i | -idle <time>     Stop if <file> unchanging for <time> sec (default = 60)
  -l | -logscale        Plot y-axis data on log scale
  -r | -refresh <time>  Refresh display every <time> sec (default = 10)
  -x | -xrange <range>  Set <range> of x-axis data, format "[0:1]"
  -y | -yrange <range>  Set <range> of y-axis data, format "[0:1]"
  -h | -help            Display short help and exit

Monitor data with Gnuplot for Splash application
For example,

    splashMonitor -l /path/to/data/file.dat

USAGE
    exit 0  # A clean exit
}

# Report error and exit
die() {
    exec 1>&2
    echo
    echo "Error encountered:"
    while [ "$#" -ge 1 ]; do echo "    $1"; shift; done
    echo
    echo "See '${0##*/} -help' for usage"
    echo
    exit 1
}

# Set Gnuplot header
plotFileHeader() {
    cat<<EOF
set term x11 1 font "helvetica,17" linewidth 1.5 persist noraise
$LOGSCALE
$XRANGE
$YRANGE
$GRID
set title "Data Monitoring"
set xlabel "$XLABEL"
plot \\
EOF
}

# Set Gnuplot footer
plotFileFooter() {
    cat<<EOF
pause $REFRESH
reread
EOF
}

# Count number of tokens in a variable
howMany() {
    ( set -f; set -- $1; echo $# )
}

#-------------------------------------------------------------------------------
IDLE=60
REFRESH=10
LOGSCALE=""
XRANGE=""
YRANGE=""
GRID=""
GNUPLOT=$(which gnuplot)
[ ! "$GNUPLOT" = "" ] || die "splashMonitor requires Gnuplot installed"

#-------------------------------------------------------------------------------

# Parse options
while [ "$#" -gt 0 ]
do
    case "$1" in
    -h | -help*)
        printHelp
        ;;
    -i | -idle)
        [ "$#" -ge 2 ] || die "'$1' option requires an argument"
        if [ -n "${2##*[!0-9]*}" ]
        then
            IDLE=$2
        else
            die "Argument of '$1' is not an integer: '$2'"
        fi
        shift 2
        ;;
    -l | -logscale)
        LOGSCALE="set logscale y"
        shift 1
        ;;
    -r | -refresh)
        [ "$#" -ge 2 ] || die "'$1' option requires an argument"
        if [ -n "${2##*[!0-9]*}" ]
        then
            REFRESH=$2
        else
            die "Argument of '$1' is not an integer: '$2'"
        fi
        shift 2
        ;;
    -x | -xrange)
        [ "$#" -ge 2 ] || die "'$1' option requires an argument"
        XRANGE="set xrange $2"
        shift 2
        ;;
    -y | -yrange)
        [ "$#" -ge 2 ] || die "'$1' option requires an argument"
        YRANGE="set yrange $2"
        shift 2
        ;;
    -g | -grid)
        GRID="set grid"
        shift 1
        ;;
    -*)
        die "unknown option: '$*'"
        ;;
    *)
        break
        ;;
    esac
done

[ "$#" -eq 1 ] || die "Incorrect arguments specified"
[ -f "$1" ]    || die "File $1 does not exit"
FILE="$1"

# Get KEYS from header
KEYS=$(grep -E '^#' "$FILE" | tail -1)

[ "$KEYS" = "" ] && KEYS="# Step"
NKEYS=$(howMany "$KEYS")
NCOLS=$(grep -m 1 '^[^#]' "$FILE" | awk '{ print NF }')

# With full column labels, NKEYS = NCOLS + 1, since it includes "#"

# If NKEYS > NCOLS + 1, REMOVE EXCESS KEYS
NCOLSPONE=$((NCOLS+1))
[ "$NKEYS" -gt "$NCOLSPONE" ] && KEYS=$(echo $KEYS | cut -d" " -f1-$NCOLSPONE)
NKEYS=$(howMany "$KEYS")

i=0
while [ "$NKEYS" -le "$NCOLS" ]
do
    i=$((i+1))
    KEYS="$KEYS data$i"
    NKEYS=$(howMany "$KEYS")
done

# Remove # and Time keys
XLABEL=$(echo $KEYS | cut -d " " -f2)
KEYS=$(echo $KEYS | cut -d " " -f3-)

GPFILE=$(mktemp)
plotFileHeader > "$GPFILE"
i=1
for field in $KEYS
do
    i=$((i+1))
    PLOTLINE="\"$FILE\" using 1:${i} with lines title \"$field\""
    if [ $i -lt $NCOLS ]
    then
       PLOTLINE="$PLOTLINE, \\"
    fi
    echo $PLOTLINE >> "$GPFILE"
done
plotFileFooter >> "$GPFILE"

touch "$FILE"
$GNUPLOT "$GPFILE" &
PID=$!

while true
do
    MODTIME=$(stat --format=%Y $FILE)
    IDLEAGO=$(($(date +%s)-IDLE))
    test "$MODTIME" -gt "$IDLEAGO" || break
    sleep $REFRESH
done

kill -9 $PID
rm -f "$GPFILE"

#--------------------------------------------------------------------------
