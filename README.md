Dophist Voice-Tag
===
Re-thought of traditional GUI
---
Modern Graphical-User-Interfaces(GUI) tend to organize operations in a hierachical tree structure, this applies on both PCs and smartphones.  
Take mobile system(android/iOS) for example:

On top level:
![tree](https://raw.github.com/dophist/launcher/master/misc/toptree.png)

Take the "Settings" child node from the above and it also has its own child nodes:
![tree](https://raw.github.com/dophist/launcher/master/misc/midtree1.png)

As another example, there are also plenty of contents under the "Phone" node:
![tree](https://raw.github.com/dophist/launcher/master/misc/midtree2.png)
Everytime you wake up your phone, you are in root node.  You can slide to switch screen.  And then you can start an app by touch the app icon under that screen.  After entering a certain app, there are also bunches of operations that you can perform.  

You probably have noticed that all operations in your GUI system are organised in __an giant tree__, which I call it __operation-tree__. In this tree, each edge represents an operation(typically touch and slide on an smartphone), and each node represents a particular state of your system.

Operation-tree could be very large. 
To give you a sense of what the entire operation-tree looks like, figures above are collected below:
![tree](https://raw.github.com/dophist/launcher/master/misc/bigtree.png)
Note that, the actual tree on your phone can be 10-100 times larger than this.

The limitation of traditional GUI
---
After getting this "tree-model" in mind, now let's think about the limitations of GUI.

Imagine you want to complete a task(reach a node in the tree), what you have to do is to travel from root node down to your target node.  

Now here comes the problem: what if a node is deep but it needs to be reached quite frequently on a daily basis?  

The fact is that users waste their time repeating meaningless operations, "travel a long way down" to some pretty frequent nodes.

If you don't get this, consider why android provides some home-screen shortcuts (or widgets) for airplane-mode, WiFi, 3G, and brightness setting.

What is Dophist Voice-Tag?
---
Dophist Voice-Tag(DVT) is a __speech-based__ UI for PC, mobile devices. It allows users to __tag a speech command to any node in the operation-tree__, such as:

For mobile phone:
* start an app/program
* make call to a friend
* activate airplane mode
* turn on/off blue-tooth
* retrieve a photo from gallery

For PC:
* start web browser and open google.com
* open a PDF/word document
* continue to play the movie that you didn't finish a few days ago
* open a music player and play a particular song that you love
* open web-brower download directory to check the file you just downloaded
etc.

After this voice-to-node binding, users can reach the node directly by repeat the corresponding speech command.

How is it different from other speech based UI?
---
1. Local, it doesn't require internet connection.  
    Almost __all__ products on the market rely on internet connection, because speech recognition is a computation-intensive task, which has to be done in server-end.  
    However, DVT is designed to be a light-weight speech UI.  A voice tagging-retrieving mechanism makes it possible to perform local recognition.
2. Fast.  
    DVT reponds extremely fast because it is local, no time is consumed to communicate with the servers.
3. Language independent.  
    English, Chinese, Spanish etc, you can use whatever language you like, DVT is not picky.
4. Accent independent.  
    DVT don't care if you have a heavy accent, it just works fine.
5. Highly customizable.  
    As a tagging system, users choose what to tag, what not to tag.  In principle, *all* operation can be tagged with user's voice.  Tags can be easily added, removed, and managed.
6. Accurate.  
    The number of "most-frequent" operations won't be large.  Say, 100 tags, DVT's recognition accuracy can reach more than 95%.
