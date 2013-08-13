Dophist Voice-Tag
===
A thought on GUI
---
Graphical-User-Interface(GUI) has been proven to be an effective and intuitive mechanism to organize and exhibit system/software operations, both on PC and smart-phone.

Why does GUI gain so much popularity?  One important reason is that GUI tries to organize possible operations in a carefully designed __tree-structure__.

Take mobile system(android/iOS) for example:

On top level:
![tree](https://raw.github.com/dophist/launcher/master/misc/toptree.png)


Child nodes from the above(such as "Settings") also have its own children:
![tree](https://raw.github.com/dophist/launcher/master/misc/midtree1.png)


As another example, the subtree of "Phone" node:
![tree](https://raw.github.com/dophist/launcher/master/misc/midtree2.png)

You probably have noticed that all operations in your GUI system are organised in __an giant tree__, which I called __operation-tree__.  In this tree, each edge represents an operation (typically touch and slide on an smartphone), and each node represents a particular state of your system/software.  

GUI is a smart design in the sense that it groups related operations layered by layer, making the all functionalities self-evident.  

To give you a sense of what the entire operation-tree looks like, figures above are collected together:
![tree](https://raw.github.com/dophist/launcher/master/misc/bigtree.png)

Note that, operation-tree could be very large, the actual tree on your phone can be 10-100 times larger than this.

Limitation of GUI
---
Keeping this "tree-model" in mind, it's now possible to consider one important limitation of GUI:

To organize the content of a whole system/software in a tree, you have a design problem:

1) _make the tree deep:_

    This means that to reach a node, you need more operations to "travel down" to your target node.

2) _make the tree broad:_

    This means that you need to distinguish your target node in the broad layer: consider finding a PDF in a directory containing 100 PDFs in PC, or finding a friend in your mobile contact.

Deepness or broadness, this is a limitation that GUI can't resolve, so here comes the problem:
__what if a node is buried so deep or hidded in a very broad layer, but it needs to be reached quite often?__

The fact is that GUI users waste their time, repeating meaningless operations, "travel down or searching" to perform some pretty frequent tasks.

If you don't get this, consider why android provides some home-screen shortcuts (or widgets) for airplane-mode, WiFi, 3G, and brightness setting; or many PC users place massive shortcuts and documents on their desktop.

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
* start web browser and open youtube.com
* open a PDF/word document
* continue to play the movie that you didn't finish a few days ago
* open a music player and play a particular song that you love
* open web-brower download directory to check the file you just downloaded
etc.

After this voice-to-node binding, users can reach a node directly by repeat the node's associating speech command.

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
