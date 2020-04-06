from utilities.itemsHelp import ItemUtilities


def populate_inv_lists(inventory_items, gameworld, item_type_in_inv):
    inv_items = []
    cnt = 0

    for item in inventory_items:
        item_type = ItemUtilities.get_item_type(gameworld=gameworld, entity=item)

        if item_type == item_type_in_inv:
            inv_items.append(item)
            if cnt == 0:
                cnt = 2
            else:
                cnt += 1

    return inv_items, cnt
