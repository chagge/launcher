Dophist Voice-Tag
===

What is Dophist Voice-Tag?
---
Dophist Voice-Tag(DVT) is a __speech-based__ UI for PC, mobile devices. It allows users to tag their speech to __any__ operation, such as:
* start an app/program
* open a PDF/word document
* start web browser and open a webpage
* make call to a friend
* turn on/off blue-tooth
* retrieve a photo from gallery

etc.

After this voice-to-operation binding, users can trigger the operation by speaking out the tagged speech.

Why voice tag?
---
1. On PC and smart-phone, all operations are organized in a tree structure, this is a illustrative figure(taking iOS for example):
![operation-tree](https://raw.github.com/dophist/launcher/master/misc/tree.png)
In this figure, each edge represents an operation(such as screen-touch activity), each tree node represents a particular state of the system.

2. To complete certain task(reach a certain node in the tree), users need to travel from the root down to their target node through step by step operations(typically touch ,slide, drag).  Theoretically, given the ability of "going back to root node", users can go to any tree node from task to task, this might be the reason why there is __only one button(HOME)__ in iPhone's hardware design.  Android devices usually provide extra buttons such as "go back a level" and "settings".

3. This operating mechanism is fine but not good enough. Every time a user wants to reach a node, he has to go through the path from root to the target node.  This means users waste their time repeating the path for frequently used nodes on a daily basis.

4. 

How is it different from other speech assistant(such as siri)?
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
