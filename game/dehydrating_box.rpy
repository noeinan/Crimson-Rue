init python:

    class DehydratorStore():

        def __init__(self):
            self.store = {}

        def add_dehydrator_data(self, **kwargs):
            self.store[kwargs["item_id"]] = kwargs

        def return_dehydrator_data(self, item):
            return Dehydrator(item=item, **self.store[item.id])

    class Dehydrator():

        def __init__(self, item, item_id, days, produces=None, inc_quality=None):
            self.item = item
            self.item_id = item_id
            self.days = days
            self.produces = produces
            self.inc_quality = inc_quality
            self.added_on = calendar.daycount_from_gamestart

        def check(self):
            if calendar.daycount_from_gamestart > self.added_on + self.days:
                item_drying_event(item=self.item)

                if self.produces:
                    player_bag.add_item(item_id=self.produces, quality=self.item.quality)
                    return "remove"

                elif self.inc_quality:
                    self.item.quality_level_up()
                    return "add_again"

            return True
            
        @property
        def days_left(self):
            return self.added_on + self.days - calendar.daycount_from_gamestart

        @property
        def get_produces(self):
            if self.inc_quality:
                return self.item
            return global_item_store.return_item(self.produces)

    class DehydratorBox():

        def __init__(self):
            self.store = []

        def add_to_box(self, item):
            if item.id not in global_dehydrator_store.store:
                item_drying_fail_event(item)
                return

            self.store.append( global_dehydrator_store.return_dehydrator_data(item) )
            player_bag.store.remove(item)

        def remove_from_box(self, item):
            player_bag.add_item(item=item.item)
            self.store.remove(item)

        def daily_check(self):
            copy_store = self.store[:]
            for entry in copy_store:
                result = entry.check()

                if result == "add_again":
                    entry.added_on = calendar.daycount_from_gamestart

                if result == "remove":
                    self.store.remove(entry)

screen drying_screen():
    tag inventory_group
    zorder 10
    modal True

    default showing = ""
    default showing_item = None
    default removeable = None

    add Solid("#000000") alpha 0.5

    textbutton _("Back") action Hide("drying_screen") xalign 1.0

    frame:
        xysize (1100, 675)
        xalign 0.5
        yalign 0.5

        background Solid("d3d3d3")

        hbox:
            spacing 5
            frame:
                area (0, 0, 570, 675)
                background None

                text "DRYING RACK" size 40 color "#000000" xalign 0.50

                vpgrid:
                    area (0, 55, 520, 500)
                    cols 4
                    spacing 25
                    draggable True
                    mousewheel True

                    scrollbars "vertical"

                    for item in player_dehydrator.store:
                        vbox:
                            spacing 5
                            button:
                                xysize (100, 100)
                                background item.item.icon

                                add item.item.get_quality_badge xalign 0.95 yalign 0.05 at zoom_out

                                action [ SetScreenVariable("showing", "item"), SetScreenVariable("showing_item", item.get_produces), If(item.inc_quality, true=SetScreenVariable("removeable", item)) ]

                            text "[item.days_left]" xalign 0.5
                            
                    if len(player_dehydrator.store) < 12:
                        for i in range(0, 12-len(player_processor.store)):
                            vbox:
                                spacing 5
                                button:
                                    xysize (100, 100)
                                    background Solid("#c0c0c0")

                                    action SetScreenVariable("showing", "inv")

                                text " "

            if showing == "inv":
                use inventory_base_screen(player_bag, "drying")
            if showing == "item":
                frame:
                    area (0, 0, 570, 675)
                    background None

                    text showing_item.name size 40 color "#000000" xalign 0.50

                    vbox:
                        xalign 0.25
                        ypos 100
                        spacing 10

                        button:
                            xysize (250, 250)
                            background showing_item.image

                            add showing_item.get_next_quality_badge xalign 0.95 yalign 0.05

                        hbox:
                            spacing 15

                            for i in showing_item.tags:
                                text i

                        if removeable:
                            textbutton _("Remove") action [ SetScreenVariable("showing", ""), SetScreenVariable("showing_item", None), Function(player_dehydrator.remove_from_box, item=removeable), If(item.inc_quality, true=SetScreenVariable("removeable", None)) ]
