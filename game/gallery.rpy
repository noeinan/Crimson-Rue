##############################################################################
# Gallery
#
# Screen that's used to display unlocked CGs. This gallery was created by leon
# from the lemmasoft forums. Thanks, leon!

init python:
    #Galleries settings - start
    #list the CG gallery images here:
    gallery_cg_items = ["cg 01", "cg 02", "cg 03", "cg 04", "cg 05", "cg 06", "cg 07", "cg 08", "cg 09", "cg 10", "cg 11"]
    
    #list the BG gallery images here (do not include variations, such as night version):
    gallery_bg_items = ["bg apothecary", "bg cellar", "bg forest001", "bg forest002", "bg forest003", "bg forest004", "bg forest005", "bg forest006", "bg forest007", "bg forest008", "bg forest009", "bg itemshop", "bg kitchen", "bg overworld01", "bg overworld02"]
    
    #how many rows and columns in the gallery screens?
    gal_rows = 3
    gal_cols = 3
    
    #thumbnail size in pixels:
    thumbnail_x = 267
    thumbnail_y = 150
    
    #the setting above (267x150) will work well with 16:9 screen ratio. Make sure to adjust it, if your are using 4:3 or something else.
    #Galleries settings - end
    
    gal_cells = gal_rows * gal_cols    
    g_cg = Gallery()
    
    for gal_item in gallery_cg_items:
        g_cg.button(gal_item + " butt")
        g_cg.image(gal_item)
        g_cg.unlock(gal_item)
    g_cg.transition = fade
    cg_page=0

    g_bg = Gallery()
    
    for gal_item in gallery_bg_items:
        g_bg.button(gal_item + " butt")
        g_bg.image(gal_item)
        g_bg.unlock(gal_item)
        
        #if BGs have variations, such as night version, uncomment the lines below and copy paste them for each BG with variations
#        if gal_item == "bg kitchen":
#            g_bg.image("bg kitchen dining")
#            g_bg.unlock("bg kitchen dining")
            
    g_bg.transition = fade
    bg_page=0
    
init +1 python:
    #Here we create the thumbnails. We create a grayscale thumbnail image for BGs, but we use a special "locked" image for CGs to prevent spoilers.
    
    for gal_item in gallery_cg_items:
        renpy.image (gal_item + " butt", im.Scale(ImageReference(gal_item), thumbnail_x, thumbnail_y))
        
    for gal_item in gallery_bg_items:
        renpy.image (gal_item + " butt", im.Scale(ImageReference(gal_item), thumbnail_x, thumbnail_y))
        renpy.image (gal_item + " butt dis", im.Grayscale(ImageReference(gal_item + " butt")))
        
screen cg_gallery:
    tag menu
    use game_menu("CG Gallery"):
        

        frame background None xpos -10:
            grid gal_rows gal_cols:
                ypos -20
                yfill True
                xfill True
                $ i = 0
                $ next_cg_page = cg_page + 1            
                if next_cg_page > int(len(gallery_cg_items)/gal_cells):
                    $ next_cg_page = 0
                for gal_item in gallery_cg_items:
                    $ i += 1
                    if i <= (cg_page+1)*gal_cells and i>cg_page*gal_cells:
                        add g_cg.make_button(gal_item + " butt", gal_item + " butt", im.Scale("gui/gallocked.png", thumbnail_x, thumbnail_y), xalign=0.5, yalign=0.5, idle_border=None, background=None, bottom_margin=24)
                for j in range(i, (cg_page+1)*gal_cells): #we need this to fully fill the grid
                    null
            frame:
                yalign 1.03
                xalign 1.005
                vbox:
                    if len(gallery_cg_items)>gal_cells:
                        textbutton _("Next Page") action [SetVariable('cg_page', next_cg_page), ShowMenu("cg_gallery")]

screen bg_gallery:
#The BG gallery screen is more or less copy pasted from the CG screen above, I only changed "make_button" to include a grayscale thumbnail for locked items
    tag menu
    use game_menu("BG Gallery"):
        frame background None xpos -10:
            grid gal_rows gal_cols:
                ypos -20
                yfill True
                xfill True
                $ i = 0
                $ next_bg_page = bg_page + 1
                if next_bg_page > int(len(gallery_bg_items)/gal_cells):
                    $ next_bg_page = 0
                for gal_item in gallery_bg_items:
                    $ i += 1
                    if i <= (bg_page+1)*gal_cells and i>bg_page*gal_cells:
                        add g_bg.make_button(gal_item + " butt", gal_item + " butt", gal_item + " butt dis", xalign=0.5, yalign=0.5, idle_border=None, background=None, bottom_margin=24)
                for j in range(i, (bg_page+1)*gal_cells):
                    null
            frame:
                yalign 1.03
                xalign 1.005
                vbox:
                    if len(gallery_bg_items)>gal_cells:
                        textbutton _("Next Page") action [SetVariable('bg_page', next_bg_page), ShowMenu("bg_gallery")]