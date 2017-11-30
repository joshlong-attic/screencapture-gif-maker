# Josh's Amazing Screen Recorder GIF Cam

## Operation

You need to have at least python 2.7, and ffmpeg installed, and the following python modules:

* futures
* moviepy
* pyscreenshot

### High Sierra (aka macOS 'Root Hole')

macOS High Sierra changes the behaviour of the fork syscall such that calls to Objective-C APIs in forked processes are treated as errors.

To alleviate, run before executing:

```
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

