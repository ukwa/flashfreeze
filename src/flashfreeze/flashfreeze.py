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

    ghost = Ghost(viewport_size=(1280, 1024))
    # ghost = Ghost(viewport_size=(1280, 1024), display=True)
    # ghost.webview.getSettings().setPluginsEnabled(true);
    page, resources = ghost.open(target)
    #assert page.http_status==200 and 'bbc' in ghost.content
    time.sleep(10)
    ghost.capture_to('original-screenshot.png')
    ghost.exit()

    # Extract a list of resource URLs
    urls = set()
    urls.add(target)
    for r in resources:
        urls.add(r.url)

    # Open pipe to the wget process
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
    for line in process.stdout:
        pass
    # Wait for the process to finish:
    process.wait()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
