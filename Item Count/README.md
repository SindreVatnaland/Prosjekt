##1# Item counting
An web-app developed for my current job.  
Its purpose is to make item counting each year more intuitive by
making it possible to register items with your phone, using a bluetooth barcode scanner, 
and add a quantity to the item.  

The item is linked to a shelve and when one is done counting a shelve
its being send from the "counting" section over to the "overview" section.  
In the overview you can go trough all finished counted shelves and register its item
in the counter from a phone rather than bringing the physical items.

Run the app and open the localhost link (Or host it on the web).  
Click on the "counting" button and from there click "New shelf",
submit and select it.  
Click "Add more items" and paste a EAN-13 code ex.(8719128117249).
The name of the item should automatically show up and you will be able to
add a quantity.  
If the item is not previously registered you will get an option to register a name.  


Quality of life:  
If you miss click the "done" button within the "overview" and the shelve is gone
you can enter "/backup" to the url for a backup (here is every fully completed shelve). 

In the "/upload" url the store can upload its full database of items
as a .xlm file and it will be automatically extracted and every EAN-code with
its respected item name to the app.
(This is how name automatically shows up when registered with its EAN-code)
  
When done you can enter the "/delete_all" url and confirm to delete
every stored shelve (even the backup), ready for a new round of counting.
