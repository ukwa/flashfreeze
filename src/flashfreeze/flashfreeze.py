from ghost import Ghost
import sys
import time
import subprocess

def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <url>\n" % (argv[0],))
        return 1

    target = argv[1]
    warc_name = "flashfrozen"

    print "Starting Ghost.py..."
    ghost = Ghost(viewport_size=(1280, 1024))
    # ghost = Ghost(viewport_size=(1280, 1024), display=True)
    # ghost.webview.getSettings().setPluginsEnabled(true);
    print "Loading page:",target
    page, resources = ghost.open(target)
    #time.sleep(2)
    print "Taking screenshot..."
    ghost.capture_to('original-screenshot.png')
    print "Shutting down Ghost.py..."
    ghost.exit()

    # Extract a list of resource URLs
    print "Extracting URLs..."
    urls = set()
    for r in resources:
        urls.add(str(r.url.toString()))
    if target not in urls:
        urls.add(target)

    # Open pipe to the wget process
    print "Passing URLs to wget..."
    process = subprocess.Popen(["wget", "-q", 
        "-i", "-", "-O", "-", 
        "--warc-file={}".format(warc_name)]
        ,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    # Also open a file to hold a note of the URLs
    urlf = open('original-urls.txt','w')
    # Pass in the URLs, via STDIN:
    for u in urls:
        urlf.write("{}\n".format(u))
        process.stdin.write("{}\n".format(u))
    # Close the URLs file:
    urlf.close()
    # Close STDIN so wget knows there are no more URLs coming:
    process.stdin.flush()
    process.stdin.close()
    # This explicitly churns through and ignores STDOUT:
    print "Waiting for wget output..."
    for line in process.stdout:
        pass
    # Wait for the process to finish:
    print "Waiting for wget to finish..."
    process.wait()

    print "Done."


if __name__ == "__main__":
    sys.exit(main(sys.argv))
