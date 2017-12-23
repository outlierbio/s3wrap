# s3wrap
Use S3 URIs as arguments for any command-line tool

# Getting started

## Installation

    pip install git+https://github.com/outlierbio/s3wrap.git
  
## Quick start
Just prefix your commands with s3wrap and substitute S3 URIs wherever you would use filepaths.

    $ s3wrap md5sum s3://bucket/file > s3://bucket/file.md5
    $ s3wrap cat s3://bucket/file1 s3://bucket/file2 > s3://your-bucket/file1_and_2
    $ s3wrap cat s3://bucket/file1_and_2 -
    <file contents>

You can also use it as a Python decorator, to swap S3 arguments for functions that expect filepaths:

    from s3wrap import s3args
    @s3args()
    def sync_and_run(*cmds):
        print('Running:\n{}'.format(' '.join(cmds)))
        return check_output(cmds)

  
## How it works
`s3wrap` is a python wrapper that examines your arguments for S3 URIs (i.e., starts with `s3://`), and follows these steps when it finds them:

- If the path is a file (does not end in a slash `/`):
  - Create a temp file
  - If the object exists on S3, consider it an input and download to the temp file
  - If the object does not exist on S3, consider it an output and upload the the temp file after the command completes.
- If the path is a folder:
  - Create a temp folder
  - If there are **any** files in the folder, consider it an input and download to the temp folder
  - If there are **no** files in the folder, consider it an output and upload the temp folder after the command completes
  
## Prefixes
Sometimes commands use prefixes, e.g., Unix `split`:

  $ echo "this is a test" > testfile
  $ split -b 5 testfile myprefix
  $ ls
  myprefixaa myprefixab myprefixac
  
Unfortunately, prefixes make it difficult for `s3wrap` to predict the exact output paths, which is necessary to automate the transfer. 

Therefore, **`s3wrap` does not support prefixes**. Only commands that exactly specify input and output paths can be wrapped by `s3wrap` at this time.

Any suggestions or pull requests (perhaps using [`inotify`](https://en.wikipedia.org/wiki/Inotify)?) are greatly appreciated!
