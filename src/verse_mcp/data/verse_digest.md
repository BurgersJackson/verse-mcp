# Verse API Digest

> **Copyright Epic Games, Inc. All Rights Reserved.**
> 
> Generated Digest of Verse API - **DO NOT modify this manually!**
> 
> Generated from build: `++Fortnite+Release-39.50-CL-50854790`

---

## Table of Contents

- [Itemization Module](#itemization-module)
- [WebAPI Module](#webapi-module)
- [SceneGraph Module](#scenegraph-module)
- [Temporary Module](#temporary-module)
  - [UI Submodule](#ui-submodule)
  - [Curves Submodule](#curves-submodule)
  - [Diagnostics Submodule](#diagnostics-submodule)
  - [SpatialMath Submodule](#spatialmath-submodule)
- [JSON Module](#json-module)
- [ControlInput Module](#controlinput-module)
- [BasicShapes Module](#basicshapes-module)
- [Assets Module](#assets-module)

---

## Itemization Module

```verse
Itemization<public> := module:
    using {/Verse.org/Assets}
    using {/Verse.org/Presentation}
    using {/Verse.org/Simulation}
    using {/Verse.org/Native}
    using {/Verse.org/SceneGraph}
```

### add_item_result

```verse
@experimental
add_item_result<native><public> := class<epic_internal>:
    # Items that were newly added to this inventory as a result of the transaction.
    AddedItems<native><public>:[]entity

    # Items whose stack size changed as a result of the transaction, and the previous stack size value.
    ModifiedItems<native><public>:[]tuple(entity, int)
```

### remove_item_result

```verse
@experimental
remove_item_result<native><public> := class<epic_internal>:
    # The inventory which the item was removed from.
    Inventory<native><public>:inventory_component

    # Total stack count of items removed as a result of this transaction.
    RemovedAmount<native><public>:int

    # Items that were removed from this inventory as a result of the transaction.
    RemovedItems<native><public>:[]entity

    # Item whose stack size changed as a result of the transaction.
    ModifiedItem<native><public>:?tuple(entity, int)
```

### equip_item_result

```verse
@experimental
equip_item_result<native><public> := class<epic_internal>:
    Item<native><public>:entity
```

### unequip_item_result

```verse
@experimental
unequip_item_result<native><public> := class<epic_internal>:
    Item<native><public>:entity
```

### find_inventory_event

When adding an item, `find_inventory_event` is used as a first pass to find the best inventory for an item. It is sent downwards. `add_item_query_event` can be used to veto inventory choices. It is sent upwards.

```verse
@experimental
find_inventory_event<native><public> := class<epic_internal>(scene_event):
    ItemComponent<native><public>:item_component

    var ChosenInventory<native><public>:?inventory_component = external {}

    var ChosenInventoryPriority<native><public>:float = external {}
```

### add_item_error

```verse
@experimental
add_item_error<native><public> := class<computes>:
```

### add_item_query_event

When adding an item, `find_inventory_event` is used as a first pass to find the best inventory for an item. It is sent downwards. `add_item_query_event` can be used to veto inventory choices. It is sent upwards.

```verse
@experimental
add_item_query_event<native><public> := class<epic_internal>(scene_event):
    Item<native><public>:item_component

    Inventory<native><public>:inventory_component

    var<private> Errors<native><public>:[]add_item_error = external {}

    AddError<public>(Error:add_item_error):void = external {}
```

### remove_item_error

```verse
@experimental
remove_item_error<native><public> := class<computes>:
```

### remove_item_query_event

```verse
@experimental
remove_item_query_event<native><public> := class<epic_internal>(scene_event):
    Item<native><public>:item_component

    Inventory<native><public>:inventory_component

    var<private> Errors<native><public>:[]remove_item_error = external {}

    AddError<public>(Error:remove_item_error):void = external {}
```

### inventory_component

Inventory components hold items. An entity with an inventory component can be considered to have an inventory. The inventory component controls which items can enter or exit. They also determine whether an item can be equipped.

```verse
@experimental
inventory_component<native><public> := class<final_super>(component):
    @available {MinUploadedAtFNVersion := 3800}
    # Adds the item to this inventory only, ignoring sub-inventories. Fails if no items could be added.
    AddItem<native><final><public>(Item:entity, ?AllowMergeItems:logic = external {})<transacts>:result(add_item_result, []add_item_error)

    @available {MinUploadedAtFNVersion := 3800}
    # Adds the item to this inventory, including sub-inventories. Fails if no items could be added.
    AddItemDistribute<native><final><public>(Item:entity, ?AllowMergeItems:logic = external {})<transacts>:result(add_item_result, []add_item_error)

    @available {MinUploadedAtFNVersion := 3800}
    # Removes an item from this inventory or its descendent inventories. Fails if the item could not be removed.
    RemoveItem<native><final><public>(Item:entity)<transacts>:result(remove_item_result, []remove_item_error)

    # Returns a list of items within this inventory only.
    GetItems<native><final><public>()<reads>:[]entity

    @available {MinUploadedAtFNVersion := 3200}
    # Returns a list of items (of a specific type) within this inventory only.
    GetItems<native><final><public>(Type:castable_subtype(item_component))<reads>:[]entity

    @available {MinUploadedAtFNVersion := 2930}
    # Returns a list of all items within this inventory and its descendant inventories.
    FindItems<native><final><public>()<reads>:generator(entity)

    @available {MinUploadedAtFNVersion := 3200}
    # Returns a list of all items (of a specific type) within this inventory and its descendant inventories.
    FindItems<native><final><public>(Type:castable_subtype(item_component))<reads>:[]entity

    # Returns a list of sub-inventories of this inventory only.
    GetInventories<native><final><public>()<reads>:[]inventory_component

    @available {MinUploadedAtFNVersion := 2930}
    # Returns a list of all sub-inventories within this inventory and its descendant inventories.
    FindInventories<native><final><public>()<reads>:generator(inventory_component)

    GetEquippedItems<final><native><public>():[]entity

    AddItemEvent<native><final><public>:listenable(add_item_result) = external {}
    RemoveItemEvent<native><final><public>:listenable(remove_item_result) = external {}
    EquipItemEvent<native><final><public>:listenable(equip_item_result) = external {}
    UnequipItemEvent<native><final><public>:listenable(unequip_item_result) = external {}
```

### CanAddItem

Returns a failure reason (such as being full) if the provided item entity cannot be added. Does not consider sub-inventories.

```verse
@available {MinUploadedAtFNVersion := 3800}
@experimental
(Inventory:inventory_component).CanAddItem<native><public>(Item:entity, ?AllowMergeItems:logic = external {})<transacts>:result(false, []add_item_error)
```

### CanAddItemDistribute

Returns a failure reason (such as being full) if the provided item entity cannot be added. AddItemDistribute allows the item to enter sub-inventories.

```verse
@available {MinUploadedAtFNVersion := 3800}
@experimental
(Inventory:inventory_component).CanAddItemDistribute<native><public>(Item:entity, ?AllowMergeItems:logic = external {})<transacts>:result(false, []add_item_error)
```

### CanRemoveItem

Returns a failure reason if the provided item is not present or cannot be removed.

```verse
@available {MinUploadedAtFNVersion := 3800}
@experimental
(Inventory:inventory_component).CanRemoveItem<native><public>(Item:entity)<transacts>:result(false, []remove_item_error)
```

### item_category

`item_category` is used to classify items.

```verse
@experimental
item_category<native><public> := class<castable><concrete><unique><final>:
```

### change_equipped_result

```verse
@experimental
change_equipped_result<native><public> := class<epic_internal>:
    ItemComponent<native><public>:item_component
    IsItemEquipped<native><public>:logic
```

### change_inventory_result

```verse
@experimental
change_inventory_result<native><public> := class<epic_internal>:
    ItemComponent<native><public>:item_component
    PreviousInventory<native><public>:?inventory_component
    CurrentInventory<native><public>:?inventory_component
```

### change_stack_size_result

```verse
@experimental
change_stack_size_result<native><public> := class<epic_internal>:
    ItemComponent<native><public>:item_component
    PreviousStackSize<native><public>:int
    CurrentStackSize<native><public>:int
```

### change_max_stack_size_result

```verse
@experimental
change_max_stack_size_result<native><public> := class<epic_internal>:
    ItemComponent<native><public>:item_component
    PreviousMaxStackSize<native><public>:?int
    CurrentMaxStackSize<native><public>:?int
```

### equip_item_error

```verse
@experimental
equip_item_error<native><public> := class<computes>:
```

### equip_item_query_event

```verse
@experimental
equip_item_query_event<native><public> := class(scene_event):
    Item<native><public>:item_component

    var<private> Errors<native><public>:[]equip_item_error = external {}

    AddError<public>(Error:equip_item_error):void = external {}
```

### unequip_item_error

```verse
@experimental
unequip_item_error<native><public> := class<computes>:
```

### unequip_item_query_event

```verse
@experimental
unequip_item_query_event<native><public> := class(scene_event):
    Item<native><public>:item_component

    var<private> Errors<native><public>:[]unequip_item_error = external {}

    AddError<public>(Error:unequip_item_error):void = external {}
```

### item_component

Anything using this component should be considered an item. Required to interact with inventories.

```verse
@experimental
item_component<native><public> := class<final_super>(component):
    OnBeginSimulation<override>():void = external {}
    OnEndSimulation<override>():void = external {}

    # Returns the inventory_component this item currently resides in. Fails if it cannot find a valid parent inventory.
    GetParentInventory<native><final><public>()<reads><decides>:inventory_component

    # Succeeds if this item is considered currently within an inventory and equipped.
    IsEquipped<native><final><public>()<reads><decides>:void

    # Broadcast when this item changes inventory.
    ChangeInventoryEvent<native><final><public>:listenable(change_inventory_result) = external {}

    # Broadcast when this item is equipped or unequipped.
    ChangeEquippedEvent<native><final><public>:listenable(change_equipped_result) = external {}

    @available {MinUploadedAtFNVersion := 3800}
    # Attempts to equip this item within the inventory it is currently in.
    # Fails if not in an inventory or if equip_item_query_event contains any errors after querying.
    Equip<final><native><public>()<transacts>:result(false, []equip_item_error)

    @available {MinUploadedAtFNVersion := 3800}
    # Attempts to unequip this item.
    # Fails if not in an inventory, not currently equipped or if unequip_item_query_event contains any errors after querying.
    Unequip<final><native><public>()<transacts>:result(false, []unequip_item_error)

    @experimental
    # Takes the specified amount of this item's stack, reducing this item's stack size in the process.
    # If taking the exact (full) amount, the item itself should be returned instead.
    # There is no default implementation of Take i.e. by default, it will fail.
    # If you want to allow this, you must override Take and return an entity containing
    # a new item_component. This new entity should not be in any inventory.
    Take<native><public>(Amount:int)<transacts><decides>:entity

    @available {MinUploadedAtFNVersion := 3200}
    # List of item_component classes we can be merged with.
    MergeableItemComponentClasses<native><public>:[]castable_subtype(item_component) = external {}

    @editable
    # Categories which this item can belong to. Note that some projects may only use the first entry.
    Categories<native><public>:[]item_category = external {}

    # Succeeds if this item can be merged into the target item. Merging an entity with itself will always fail.
    CanMergeInto<final><native_callable><public>(TargetItem:entity)<reads><decides>:void = external {}

    # Attempts to merge this item into the specified item. Fails if items cannot be merged or no items are moved.
    # If TargetAmount is specified, only that amount will try to be merged into this item.
    MergeInto<final><native_callable><public>(TargetItem:entity, ?TargetAmount:?int = external {})<transacts><decides>:void = external {}

    @editable_number(int) {MinValue := option {1}}
    # Current stack size of this item.
    var<private> StackSize<native><public>:int = external {}

    # Sets the stack size of this item.
    SetStackSize<final><native><public>(NewStackSize:int)<transacts>:void

    @editable
    # Maximum stack size for this item.
    var<private> MaxStackSize<native><public>:?int = external {}

    # Sets the maximum stack size for this item. If ClampStackSize is true, StackSize will be clamped to NewMaxStackSize.
    SetMaxStackSize<final><native><public>(NewMaxStackSize:int, ?ClampStackSize:logic = external {})<transacts>:void

    ChangeStackSizeEvent<native><final><public>:listenable(change_stack_size_result) = external {}
    ChangeMaxStackSizeEvent<native><final><public>:listenable(change_max_stack_size_result) = external {}

    # Removes the item from its inventory and places it in the simulation world. Works on orphaned items i.e. outside the world or any inventory.
    # Fails if the item is already a pickup. The transform of the item will not be altered except to unparent it from any inventory.
    (/UnrealEngine.com/Itemization/item_component:)Drop<native><public>()<transacts><decides>:void

    # Fails if this item is already in an inventory, or the inventory cannot accept the item.
    PickUp<native><public>(Inventory:inventory_component)<transacts><decides>:void
```

### CanEquip / CanUnequip

```verse
@available {MinUploadedAtFNVersion := 3800}
@experimental
(Item:item_component).CanEquip<native><public>()<transacts>:result(false, []equip_item_error)

@available {MinUploadedAtFNVersion := 3800}
@experimental
(Item:item_component).CanUnequip<native><public>()<transacts>:result(false, []unequip_item_error)
```

### has_item_merge_rules

Item Merge Rules Interface. Implemented by components that want to participate in item mergeability checks.

```verse
@experimental
has_item_merge_rules<public> := interface<unique>:
    CanMergeInto<public>(TargetItem:entity)<reads><decides>:void = external {}
    OnMergeInto<public>(TargetItem:entity, MergeAmount:int)<transacts>:void = external {}
```

### item_details_component

Component that holds the details of an item.

```verse
@experimental
item_details_component<native><public> := class<final_super>(component, has_description):
    var Name<override>:message = external {}
    var Description<override>:message = external {}
    var ShortDescription<override>:message = external {}

    OnBeginSimulation<override>():void = external {}
    OnEndSimulation<override>():void = external {}
```

### item_icon_component

Component that holds the icon for an item.

```verse
@experimental
item_icon_component<native><public> := class<final_super>(component, has_icon):
    OnBeginSimulation<override>():void = external {}
    OnEndSimulation<override>():void = external {}
```

---

## WebAPI Module

### client_id

Usage:
- Licensed users create a derived version of `client_id` in their module.
- The Verse class path for your derived `client_id` is then used as the configuration key in your backend service to map to your endpoint.

**WARNING:** do not make your derived `client_id` class public. This object type is your private key to your backend.

Example:
```verse
my_client_id<internal> := class<final><computes>(client_id)
MyClient<internal> := MakeClient(my_client_id)
```

```verse
client_id<native><public> := class<abstract><computes>:

client<native><public> := class<final><computes><internal>:
    Get<native><public>(Path:string)<suspends>:response

response<native><public> := class<internal>:

body_response<native><public> := class<internal>(response):
    GetBody<native><public>()<computes>:string

MakeClient<native><public>(ClientId:client_id)<converges>:client
```

---

## SceneGraph Module

Module import path: `/UnrealEngine.com/SceneGraph`

```verse
(/UnrealEngine.com:)SceneGraph<public> := module:
    using {/Verse.org/Native}
```

---

## Temporary Module

### UI Submodule

Module import path: `/UnrealEngine.com/Temporary/UI`

```verse
(/UnrealEngine.com/Temporary:)UI<public> := module:
    using {/Verse.org/Colors}
    using {/Verse.org/Assets}
    using {/UnrealEngine.com/Temporary/SpatialMath}
    using {/Verse.org/Simulation}
```

#### GetPlayerUI

Returns the `player_ui` associated with `Player`. Fails if there is no `player_ui` associated with `Player`.

```verse
GetPlayerUI<native><public>(Player:player)<transacts><decides>:player_ui
```

#### player_ui

The main interface for adding and removing `widget`s to a player's UI.

```verse
player_ui<native><public> := class<final><epic_internal>:
    # Adds `Widget` to this `player_ui` using default `player_ui_slot` configuration options.
    AddWidget<native><public>(Widget:widget):void

    # Adds `Widget` to this `player_ui` using `Slot` for configuration options.
    AddWidget<native><public>(Widget:widget, Slot:player_ui_slot):void

    # Removes `Widget` from this `player_ui`.
    RemoveWidget<native><public>(Widget:widget):void

    # Sets the user's focus on this `Widget`. The target `Widget` must be focusable, otherwise this has no effect.
    SetFocus<native><public>(Widget:widget):void
```

#### widget

Base class for all UI elements drawn on the `player`'s screen.

```verse
widget<native><public> := class<abstract><unique><epic_internal>:
    # Shows or hides the `widget` without removing itself from the containing `player_ui`.
    SetVisibility<native><public>(InVisibility:widget_visibility):void

    # Returns the current `widget_visibility` state.
    GetVisibility<native><public>():widget_visibility

    # Enables or disables whether the `player` can interact with this `widget`.
    SetEnabled<native><public>(InIsEnabled:logic):void

    # `true` if this `widget` can be modified interactively by the player.
    IsEnabled<native><public>():logic

    # Returns the `widget`'s parent `widget`.
    GetParentWidget<native><public>()<transacts><decides>:widget

    # Returns the `widget` that added this `widget` to the `player_ui`.
    GetRootWidget<native><public>()<transacts><decides>:widget
```

#### player_ui_slot

`widget` creation configuration options.

```verse
player_ui_slot<native><public> := struct:
    # Controls `widget` rendering order. Greater values will be draw in front of lesser values.
    ZOrder<native><public>:type {_X:int where 0 <= _X, _X <= 2147483647} = external {}

    # Controls `widget` input event consumption.
    InputMode<native><public>:ui_input_mode = external {}
```

#### ui_input_mode

`widget` input consumption mode.

| Value | Description |
|-------|-------------|
| `None` | `widget` does not consume any input |
| `All` | `widget` consumes all inputs |

```verse
ui_input_mode<native><public> := enum:
    None
    All
```

#### widget_message

Parameters for `event`s signalled by a `widget`.

```verse
widget_message<native><public> := struct:
    Player<native><public>:player
    Source<native><public>:widget
```

#### widget_visibility

| Value | Description |
|-------|-------------|
| `Visible` | The `widget` is visible and occupies layout space |
| `Collapsed` | The `widget` is invisible and does not occupy layout space |
| `Hidden` | The `widget` is invisible and occupies layout space |

```verse
widget_visibility<native><public> := enum:
    Visible
    Collapsed
    Hidden
```

#### orientation

| Value | Description |
|-------|-------------|
| `Horizontal` | Orient `widget`s from left to right |
| `Vertical` | Orient `widget`s from top to bottom |

```verse
orientation<native><public> := enum:
    Horizontal
    Vertical
```

#### horizontal_alignment

| Value | Description |
|-------|-------------|
| `Center` | Center `widget` horizontally within the slot |
| `Left` | Align `widget` to the left of the slot |
| `Right` | Align `widget` to the right of the slot |
| `Fill` | `widget` fills the slot horizontally |

```verse
horizontal_alignment<native><public> := enum:
    Center
    Left
    Right
    Fill
```

#### vertical_alignment

| Value | Description |
|-------|-------------|
| `Center` | Center `widget` vertically within the slot |
| `Top` | Align `widget` to the top of the slot |
| `Bottom` | Align `widget` to the bottom of the slot |
| `Fill` | `widget` fills the slot vertically |

```verse
vertical_alignment<native><public> := enum:
    Center
    Top
    Bottom
    Fill
```

#### anchors

The anchors of a `widget` determine its position and sizing relative to its parent. Range: `(0.0, 0.0)` (left, top) to `(1.0, 1.0)` (right, bottom).

```verse
anchors<native><public> := struct:
    Minimum<native><public>:vector2 = external {}  # (left, top)
    Maximum<native><public>:vector2 = external {}  # (right, bottom)
```

#### margin

Specifies the gap outside each edge separating a `widget` from its neighbors. Distance is measured in units where `1.0` unit is the width of a pixel at 1080p resolution.

```verse
margin<native><public> := struct:
    Left<native><public>:float = external {}
    Top<native><public>:float = external {}
    Right<native><public>:float = external {}
    Bottom<native><public>:float = external {}
```

#### button

Button is a container of a single child widget slot and fires the OnClick event when the button is clicked.

```verse
button<native><public> := class<final>(widget):
    Slot<native><public>:button_slot
    SetWidget<native><public>(InSlot:button_slot):void

    OnClick<public>():listenable(widget_message) = external {}
    HighlightEvent<public>():listenable(widget_message) = external {}
    UnhighlightEvent<public>():listenable(widget_message) = external {}

    @experimental
    var TriggeringInputAction<public>:?input_action(logic) = external {}
```

#### button_slot

```verse
button_slot<native><public> := struct:
    Widget<native><public>:widget
    HorizontalAlignment<native><public>:horizontal_alignment = external {}
    VerticalAlignment<native><public>:vertical_alignment = external {}
    Padding<native><public>:margin = external {}
```

#### canvas

Canvas is a container widget that allows for arbitrary positioning of widgets in the canvas' slots.

```verse
canvas<native><public> := class<final>(widget):
    Slots<native><public>:[]canvas_slot = external {}
    AddWidget<native><public>(Slot:canvas_slot):void
    RemoveWidget<native><public>(Widget:widget):void
```

#### canvas_slot

```verse
canvas_slot<native><public> := struct:
    Anchors<native><public>:anchors = external {}
    Offsets<native><public>:margin = external {}
    SizeToContent<native><public>:logic = external {}
    Alignment<native><public>:vector2 = external {}
    ZOrder<native><public>:type {_X:int where 0 <= _X, _X <= 2147483647} = external {}
    Widget<native><public>:widget
```

#### MakeCanvasSlot

Make a canvas slot for fixed position widget. If Size is set, then Offsets is calculated and SizeToContent is set to false. If Size is not set, then Right and Bottom are set to zero and are not used. The widget size will be automatically calculated.

```verse
MakeCanvasSlot<native><public>(Widget:widget, Position:vector2, ?Size:vector2 = external {}, ?ZOrder:type {_X:int where 0 <= _X, _X <= 2147483647} = external {}, ?Alignment:vector2 = external {})<computes>:canvas_slot
```

#### color_block

A solid color widget.

```verse
color_block<native><public> := class<final>(widget):
    DefaultColor<native><public>:color = external {}
    DefaultOpacity<native><public>:type {_X:float where 0.000000 <= _X, _X <= 1.000000} = external {}
    DefaultDesiredSize<native><public>:vector2 = external {}

    SetColor<native><public>(InColor:color):void
    GetColor<native><public>():color
    SetOpacity<native><public>(InOpacity:type {_X:float where 0.000000 <= _X, _X <= 1.000000}):void
    GetOpacity<native><public>():type {_X:float where 0.000000 <= _X, _X <= 1.000000}
    SetDesiredSize<native><public>(InDesiredSize:vector2):void
    GetDesiredSize<native><public>():vector2
```

#### image_tiling

| Value | Description |
|-------|-------------|
| `Stretch` | Stretch the image to fit the available space |
| `Repeat` | Repeat/Wrap the image to fill the available space |

```verse
image_tiling<native><public> := enum:
    Stretch
    Repeat
```

#### texture_block

A widget to display a texture.

```verse
texture_block<native><public> := class(widget):
    DefaultImage<native><public>:texture
    DefaultTint<native><public>:color = external {}
    DefaultDesiredSize<native><public>:vector2 = external {}
    DefaultHorizontalTiling<native><public>:image_tiling = external {}
    DefaultVerticalTiling<native><public>:image_tiling = external {}

    SetImage<native><public>(InImage:texture):void
    GetImage<native><public>():texture
    SetTint<native><public>(InColor:color):void
    GetTint<native><public>():color
    SetDesiredSize<native><public>(InDesiredSize:vector2):void
    GetDesiredSize<native><public>():vector2
    SetTiling<native><public>(InHorizontalTiling:image_tiling, InVerticalTiling:image_tiling):void
    GetTiling<native><public>():tuple(image_tiling, image_tiling)
```

#### material_block

A widget to display a material.

```verse
material_block<native><public> := class(widget):
    DefaultImage<native><public>:material
    DefaultTint<native><public>:color = external {}
    DefaultDesiredSize<native><public>:vector2 = external {}

    SetImage<native><public>(InImage:material):void
    GetImage<native><public>():material
    SetTint<native><public>(InColor:color):void
    GetTint<native><public>():color
    SetDesiredSize<native><public>(InDesiredSize:vector2):void
    GetDesiredSize<native><public>():vector2
```

#### overlay

Overlay is a container consisting of widgets stacked on top of each other.

```verse
overlay<native><public> := class<final>(widget):
    Slots<native><public>:[]overlay_slot = external {}
    AddWidget<native><public>(Slot:overlay_slot):void
    RemoveWidget<native><public>(Widget:widget):void
```

#### overlay_slot

```verse
overlay_slot<native><public> := struct:
    Widget<native><public>:widget
    HorizontalAlignment<native><public>:horizontal_alignment = external {}
    VerticalAlignment<native><public>:vertical_alignment = external {}
    Padding<native><public>:margin = external {}
```

#### stack_box

Stack box is a container of a list of widgets stacked either vertically or horizontally.

```verse
stack_box<native><public> := class<final>(widget):
    Slots<native><public>:[]stack_box_slot = external {}
    Orientation<native><public>:orientation
    AddWidget<native><public>(Slot:stack_box_slot):void
    RemoveWidget<native><public>(Widget:widget):void
```

#### stack_box_slot

```verse
stack_box_slot<native><public> := struct:
    Widget<native><public>:widget
    HorizontalAlignment<native><public>:horizontal_alignment = external {}
    VerticalAlignment<native><public>:vertical_alignment = external {}
    Padding<native><public>:margin = external {}
    Distribution<native><public>:?float = external {}
```

#### text_justification

| Value | Description |
|-------|-------------|
| `Left` | Justify text logically to the left based on current culture |
| `Center` | Justify text in the center |
| `Right` | Justify text logically to the right based on current culture |
| `InvariantLeft` | Always left |
| `InvariantRight` | Always right |

```verse
text_justification<native><public> := enum:
    Left
    Center
    Right
    InvariantLeft
    InvariantRight
```

#### text_overflow_policy

| Value | Description |
|-------|-------------|
| `Clip` | Overflowing text will be clipped |
| `Ellipsis` | Overflowing text will be replaced with an ellipsis |

```verse
text_overflow_policy<native><public> := enum:
    Clip
    Ellipsis
```

#### text_base

Base widget for text widget.

```verse
text_base<native><public> := class<abstract>(widget):
    DefaultText<native><localizes><public>:message = external {}
    DefaultTextColor<native><public>:color = external {}
    DefaultTextSize<native><public>:float = external {}
    DefaultTextOpacity<native><public>:type {_X:float where 0.000000 <= _X, _X <= 1.000000} = external {}
    DefaultJustification<native><public>:text_justification = external {}
    DefaultOverflowPolicy<native><public>:text_overflow_policy = external {}

    SetText<native><public>(InText:message):void
    GetText<native><public>():string
    SetJustification<native><public>(InJustification:text_justification):void
    GetJustification<native><public>():text_justification
    SetOverflowPolicy<native><public>(InOverflowPolicy:text_overflow_policy):void
    GetOverflowPolicy<native><public>():text_overflow_policy
    SetTextColor<native><public>(InColor:color):void
    GetTextColor<native><public>():color
    SetTextSize<native><public>(InSize:float):void
    GetTextSize<native><public>():float
    SetTextOpacity<native><public>(InOpacity:type {_X:float where 0.000000 <= _X, _X <= 1.000000}):void
    GetTextOpacity<native><public>():type {_X:float where 0.000000 <= _X, _X <= 1.000000}
```

---

### Curves Submodule

Module import path: `/UnrealEngine.com/Temporary/Curves`

```verse
Curves<public> := module:
    editable_curve<native><public> := class<final><concrete>:
        # Evaluates this float curve at the specified time and returns the result as a float
        Evaluate<native><public>(Time:float):float
```

---

### Diagnostics Submodule

Module import path: `/UnrealEngine.com/Temporary/Diagnostics`

```verse
Diagnostics<public> := module:
    using {/UnrealEngine.com/Temporary/SpatialMath}
    using {/Verse.org/Colors}
    using {/Verse.org/SpatialMath}
```

#### debug_draw_duration_policy

| Value | Description |
|-------|-------------|
| `SingleFrame` | Draw for a single frame |
| `FiniteDuration` | Draw for a specified duration |
| `Persistent` | Draw persistently |

```verse
debug_draw_duration_policy<native><public> := enum:
    SingleFrame
    FiniteDuration
    Persistent
```

#### debug_draw_channel

Base class used to define debug draw channels.

```verse
debug_draw_channel<native><public> := class<abstract>:
```

#### debug_draw

Debug draw class to draw debug shapes on screen.

```verse
debug_draw<native><public> := class:
    Channel<native><public>:subtype(debug_draw_channel) = external {}
    
    ShowChannel<native><public>()<transacts>:void
    HideChannel<native><public>()<transacts>:void
    ClearChannel<native><public>()<transacts>:void
    Clear<native><public>()<transacts>:void

    DrawSphere<native><public>(Center:vector3, ?Radius:float, ?Color:color, ?NumSegments:int, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawBox<native><public>(Center:vector3, Rotation:rotation, ?Extent:vector3, ?Color:color, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawCapsule<native><public>(Center:vector3, Rotation:rotation, ?Height:float, ?Radius:float, ?Color:color, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawCone<native><public>(Origin:vector3, Direction:vector3, ?Height:float, ?NumSides:int, ?AngleWidthRadians:float, ?AngleHeightRadians:float, ?Color:color, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawCylinder<native><public>(Start:vector3, End:vector3, ?NumSegments:int, ?Radius:float, ?Color:color, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawLine<native><public>(Start:vector3, End:vector3, ?Color:color, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawPoint<native><public>(Position:vector3, ?Color:color, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawArrow<native><public>(Start:vector3, End:vector3, ?ArrowSize:float, ?Color:color, ?Thickness:float, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float)<transacts>:void
    DrawText<native><public>(Text:string, Position:vector3, ?Color:color, ?DrawDurationPolicy:debug_draw_duration_policy, ?Duration:float, ?FontScale:float, ?DrawDropShadow:logic)<transacts>:void
```

#### log_level

| Value |
|-------|
| `Debug` |
| `Verbose` |
| `Normal` |
| `Warning` |
| `Error` |

```verse
log_level<native><public> := enum:
    Debug
    Verbose
    Normal
    Warning
    Error
```

#### log_channel

Base class used to define log channels. The class name will be prefixed to output messages.

```verse
log_channel<native><public> := class<abstract>:
```

#### log

```verse
log<native><public> := class:
    Channel<native><public>:subtype(log_channel)
    DefaultLevel<native><public>:log_level = external {}

    Print<public>(Message:string, ?Level:log_level)<computes>:void = external {}
    Print<public>(Message:diagnostic, ?Level:log_level)<computes>:void = external {}
    PrintCallStack<native><public>(?Level:log_level)<computes>:void
```

---

### SpatialMath Submodule

Module import path: `/UnrealEngine.com/Temporary/SpatialMath`

```verse
(/UnrealEngine.com/Temporary:)SpatialMath<public> := module:
    using {/Verse.org/SpatialMath}
    using {/Verse.org/Native}
    using {/Verse.org/Simulation}
```

#### rotation

```verse
@editable
@import_as("/Script/EpicGamesTemporary.FVerseRotation_Deprecated")
rotation<native><public> := struct<concrete>:
```

#### MakeRotation

Makes a `rotation` from `Axis` and `AngleRadians` using a left-handed sign convention (e.g. a positive rotation around +Z takes +X to +Y). If `Axis.IsAlmostZero[]`, make the identity rotation.

```verse
MakeRotation<native><public>(Axis:vector3, AngleRadians:float)<reads><converges>:rotation
```

#### MakeRotationFromYawPitchRollDegrees

Makes a `rotation` by applying in order:
1. **Yaw** about the Z axis (positive = clockwise when viewed from above)
2. **Pitch** about the new Y axis (positive = nose up)
3. **Roll** about the new X axis (positive = clockwise when viewed along +X)

```verse
MakeRotationFromYawPitchRollDegrees<native><public>(YawRightDegrees:float, PitchUpDegrees:float, RollClockwiseDegrees:float)<reads><converges>:rotation
```

#### IdentityRotation

```verse
IdentityRotation<native><public>()<converges>:rotation
```

#### Distance

Returns the 'distance' between two rotations (0.0 = equivalent, 1.0 = 180 degrees apart).

```verse
Distance<native><public>(Rotation1:rotation, Rotation2:rotation)<reads>:float
```

#### AngularDistance

Returns the smallest angular distance between rotations in radians.

```verse
AngularDistance<native><public>(Rotation1:rotation, Rotation2:rotation)<reads>:float
```

#### Rotation Methods

```verse
(InitialRotation:rotation).ApplyPitch<native><public>(PitchUpRadians:float)<transacts>:rotation
(InitialRotation:rotation).ApplyRoll<native><public>(RollClockwiseRadians:float)<transacts>:rotation
(InitialRotation:rotation).ApplyYaw<native><public>(YawRightRadians:float)<transacts>:rotation
(InitialRotation:rotation).ApplyWorldRotationX<native><public>(AngleRadians:float)<transacts>:rotation
(InitialRotation:rotation).ApplyWorldRotationY<native><public>(AngleRadians:float)<transacts>:rotation
(InitialRotation:rotation).ApplyWorldRotationZ<native><public>(AngleRadians:float)<transacts>:rotation
(InitialRotation:rotation).ApplyLocalRotationY<public>(AngleRadians:float)<transacts>:rotation = external {}
(InitialRotation:rotation).ApplyLocalRotationZ<public>(AngleRadians:float)<transacts>:rotation = external {}
(InitialRotation:rotation).RotateBy<native><public>(AdditionalRotation:rotation)<transacts>:rotation
(InitialRotation:rotation).UnrotateBy<native><public>(RotationToRemove:rotation)<transacts>:rotation
(Rotation:rotation).GetYawPitchRollDegrees<native><public>()<reads>:[]float
(Rotation:rotation).GetAxis<native><public>()<reads>:vector3
(Rotation:rotation).GetAngle<native><public>()<reads>:float
(Rotation:rotation).RotateVector<native><public>(Vector:vector3)<reads>:vector3
(Rotation:rotation).UnrotateVector<native><public>(Vector:vector3)<reads>:vector3
(Rotation:rotation).Invert<native><public>()<transacts>:rotation
(Rotation:rotation).IsFinite<native><public>()<decides><converges>:rotation
(Rotation:rotation).GetLocalForward<public>()<transacts>:vector3 = external {}
(Rotation:rotation).GetLocalRight<public>()<transacts>:vector3 = external {}
(Rotation:rotation).GetLocalUp<public>()<transacts>:vector3 = external {}
```

#### MakeShortestRotationBetween

```verse
MakeShortestRotationBetween<native><public>(InitialRotation:rotation, FinalRotation:rotation)<transacts>:rotation
MakeShortestRotationBetween<native><public>(InitialVector:vector3, FinalVector:vector3)<transacts>:rotation
```

#### MakeComponentWiseDeltaRotation

```verse
MakeComponentWiseDeltaRotation<native><public>(RotationA:rotation, RotationB:rotation)<transacts>:rotation
```

#### Slerp

Spherical linear interpolation between rotations.

```verse
Slerp<native><public>(InitialRotation:rotation, FinalRotation:rotation, Parameter:float)<transacts><decides>:rotation
```

#### Utility Functions

```verse
ToString<public>(Rotation:rotation)<reads>:string = external {}
DegreesToRadians<public>(Degrees:float)<reads>:float = external {}
RadiansToDegrees<public>(Radians:float)<reads>:float = external {}
```

#### Conversion Functions (Temporary <-> Verse SpatialMath)

```verse
@available {MinUploadedAtFNVersion := 3400}
FromVector3<public>(InVector3:vector3)<reads>:(/Verse.org/SpatialMath:)vector3 = external {}

@available {MinUploadedAtFNVersion := 3600}
FromScalarVector3<public>(InVector3:vector3)<reads>:(/Verse.org/SpatialMath:)vector3 = external {}

@available {MinUploadedAtFNVersion := 3400}
FromRotation<public>(InRotation:rotation)<reads>:(/Verse.org/SpatialMath:)rotation = external {}

@available {MinUploadedAtFNVersion := 3400}
FromTransform<public>(InTransform:transform)<reads>:(/Verse.org/SpatialMath:)transform = external {}

@available {MinUploadedAtFNVersion := 3400}
FromVector3<public>(InVector3:(/Verse.org/SpatialMath:)vector3)<reads>:vector3 = external {}

@available {MinUploadedAtFNVersion := 3600}
FromScalarVector3<public>(InVector3:(/Verse.org/SpatialMath:)vector3)<reads>:vector3 = external {}

@available {MinUploadedAtFNVersion := 3400}
FromRotation<public>(InRotation:(/Verse.org/SpatialMath:)rotation)<reads>:rotation = external {}

@available {MinUploadedAtFNVersion := 3400}
FromTransform<public>(InTransform:(/Verse.org/SpatialMath:)transform)<reads>:transform = external {}
```

#### transform

A combination of scale, rotation, and translation, applied in that order.

```verse
transform<native><public> := struct<concrete><computes>:
    @editable
    Scale<native><public>:vector3 = external {}

    @editable
    Rotation<native><public>:rotation = external {}

    @editable
    Translation<native><public>:vector3 = external {}
```

#### TransformVector

```verse
TransformVector<public>(InTransform:transform, InVector:vector3)<reads>:vector3 = external {}
TransformVectorNoScale<public>(InTransform:transform, InVector:vector3)<reads>:vector3 = external {}
```

#### vector2

2-dimensional vector with `float` components.

```verse
vector2<native><public> := struct<concrete><computes><persistable>:
    @editable
    X<native><public>:float = external {}

    @editable
    Y<native><public>:float = external {}
```

##### vector2 Functions

```verse
ReflectVector<public>(Direction:vector2, SurfaceNormal:vector2)<reads><decides>:vector2 = external {}
DotProduct<public>(V1:vector2, V2:vector2)<reads>:float = external {}
Distance<public>(V1:vector2, V2:vector2)<reads>:float = external {}
DistanceSquared<public>(V1:vector2, V2:vector2)<reads>:float = external {}
(V:vector2).MakeUnitVector<public>()<reads><decides>:vector2 = external {}
(V:vector2).Length<public>()<reads>:float = external {}
(V:vector2).LengthSquared<public>()<reads>:float = external {}
Lerp<public>(From:vector2, To:vector2, Parameter:float)<reads>:vector2 = external {}
ToString<public>(V:vector2)<reads>:string = external {}

# Operators
prefix'-'<public>(Operand:vector2)<computes>:vector2 = external {}
operator'+'<public>(Left:vector2, Right:vector2)<computes>:vector2 = external {}
operator'-'<public>(Left:vector2, Right:vector2)<computes>:vector2 = external {}
operator'*'<public>(Left:vector2, Right:float)<computes>:vector2 = external {}
operator'*'<public>(Left:float, Right:vector2)<computes>:vector2 = external {}
operator'/'<public>(Left:vector2, Right:float)<computes>:vector2 = external {}
operator'/'<public>(Left:vector2, Right:vector2)<computes>:vector2 = external {}

ToVector2<public>(V:vector2i)<transacts>:vector2 = external {}
(V:vector2).IsFinite<public>()<computes><decides>:vector2 = external {}
(V:vector2).IsAlmostZero<public>(AbsoluteTolerance:float)<computes><decides>:void = external {}
IsAlmostEqual<public>(V1:vector2, V2:vector2, AbsoluteTolerance:float)<computes><decides>:void = external {}
```

#### vector2i

2-dimensional vector with `int` components.

```verse
vector2i<native><public> := struct<concrete><computes><persistable>:
    @editable
    X<native><public>:int = external {}

    @editable
    Y<native><public>:int = external {}
```

##### vector2i Functions

```verse
DotProduct<public>(V1:vector2i, V2:vector2i)<computes>:int = external {}
Equals<public>(V1:vector2i, V2:vector2i)<computes><decides>:vector2i = external {}
ToString<public>(V:vector2i)<computes>:string = external {}
ToVector2i<public>(V:vector2)<reads><decides>:vector2i = external {}

# Operators
prefix'-'<public>(Operand:vector2i)<computes>:vector2i = external {}
operator'+'<public>(Left:vector2i, Right:vector2i)<computes>:vector2i = external {}
operator'-'<public>(Left:vector2i, Right:vector2i)<computes>:vector2i = external {}
operator'*'<public>(Left:vector2i, Right:int)<computes>:vector2i = external {}
operator'*'<public>(Left:int, Right:vector2i)<computes>:vector2i = external {}
```

#### vector3

3-dimensional vector with `float` components.

```verse
vector3<native><public> := struct<concrete><computes><persistable>:
    @editable
    X<native><public>:float = external {}

    @editable
    Y<native><public>:float = external {}

    @editable
    Z<native><public>:float = external {}
```

##### vector3 Functions

```verse
ReflectVector<public>(Direction:vector3, SurfaceNormal:vector3)<reads><decides>:vector3 = external {}
DotProduct<public>(V1:vector3, V2:vector3)<reads>:float = external {}
CrossProduct<public>(V1:vector3, V2:vector3)<reads>:vector3 = external {}
Distance<public>(V1:vector3, V2:vector3)<reads>:float = external {}
DistanceSquared<public>(V1:vector3, V2:vector3)<reads>:float = external {}
DistanceXY<public>(V1:vector3, V2:vector3)<reads>:float = external {}
DistanceSquaredXY<public>(V1:vector3, V2:vector3)<reads>:float = external {}
(V:vector3).MakeUnitVector<public>()<reads><decides>:vector3 = external {}
ToString<public>(V:vector3)<reads>:string = external {}
(V:vector3).Length<public>()<reads>:float = external {}
(V:vector3).LengthSquared<public>()<computes>:float = external {}
(V:vector3).LengthXY<public>()<reads>:float = external {}
(V:vector3).LengthSquaredXY<public>()<reads>:float = external {}
Lerp<public>(From:vector3, To:vector3, Parameter:float)<reads>:vector3 = external {}

# Operators
prefix'-'<public>(Operand:vector3)<computes>:vector3 = external {}
operator'+'<public>(L:vector3, R:vector3)<computes>:vector3 = external {}
operator'-'<public>(L:vector3, R:vector3)<computes>:vector3 = external {}
operator'*'<public>(L:vector3, R:vector3)<computes>:vector3 = external {}
operator'*'<public>(L:vector3, R:float)<computes>:vector3 = external {}
operator'*'<public>(L:float, R:vector3)<computes>:vector3 = external {}
operator'/'<public>(L:vector3, R:float)<computes>:vector3 = external {}
operator'/'<public>(L:vector3, R:vector3)<computes>:vector3 = external {}

(V:vector3).IsFinite<public>()<computes><decides>:vector3 = external {}
(V:vector3).IsAlmostZero<public>(AbsoluteTolerance:float)<computes><decides>:void = external {}
IsAlmostEqual<public>(V1:vector3, V2:vector3, AbsoluteTolerance:float)<computes><decides>:void = external {}
```

---

### SortBy

Stably sort `Array` using `Less` where `Less` succeeding indicates `Left` should precede `Right`.

```verse
SortBy<native><public>((Array:[]t, Less:type {_(:t, :t)<computes><decides>:void}) where t:type)<computes>:[]t
```

---

## JSON Module

```verse
JSON<public> := module:
    value<native><public> := class:
        AsObject<native><public>()<transacts><decides>:[string]value
        AsArray<native><public>()<transacts><decides>:[]value
        AsInt<native><public>()<transacts><decides>:int
        AsFloat<native><public>()<transacts><decides>:float
        AsString<native><public>()<transacts><decides>:string
        AsNull<native><public>()<transacts><decides>:void

    # Parse a JSON string returning a value with its contents
    Parse<native><public>(JSONString:string)<transacts><decides>:value
```

---

## ControlInput Module

Module import path: `/UnrealEngine.com/ControlInput`

```verse
ControlInput<public> := module:
    using {/Verse.org/Assets}
    using {/Verse.org/Native}
    using {/Verse.org/Simulation}
```

### input_events

Container for user input events which can be subscribed to.

**Flow:**
```
DetectionBeginEvent -> DetectionOngoingEvent -> ActivationTriggeredEvent -> DetectionEndEvent
         /\                    /\                                                   /
           \----------------> ActivationCanceledEvent -----------------------------/
```

```verse
@available {MinUploadedAtFNVersion := 3630}
input_events<native><public>(t:type) := class<epic_internal>:
    # This input has met all required conditions and has successfully fired.
    ActivationTriggeredEvent<native><public>:listenable(tuple(player, t)) = external {}

    # This input has been canceled before activation.
    ActivationCanceledEvent<native><public>:listenable(tuple(player, t, float)) = external {}

    # Detection has started for this input.
    DetectionBeginEvent<native><public>:listenable(tuple(player, t)) = external {}

    # Detection for this input is still being processed.
    DetectionOngoingEvent<native><public>:listenable(tuple(player, t, float)) = external {}

    # Detection has finished.
    DetectionEndEvent<native><public>:listenable(tuple(player, float)) = external {}
```

### GetPlayerInput

Access input-related data and settings for a player.

```verse
@available {MinUploadedAtFNVersion := 3630}
GetPlayerInput<native><public>(Player:player)<transacts><decides>:player_input
```

### player_input

Main manager class for input-related settings and functions for a player.

```verse
@available {MinUploadedAtFNVersion := 3630}
player_input<native><public> := class:
    AddInputMapping<native><public>(InputMapping:input_mapping):void
    RemoveInputMapping<native><public>(InputMapping:input_mapping):void
    GetInputEvents<native><public>(ActionToBind:input_action(t) where t:type):input_events(t)
```

### UI Submodule (ControlInput)

Module import path: `/UnrealEngine.com/ControlInput/UI`

#### Menu Navigation

```verse
@experimental
MenuNavigationMapping<public>:input_mapping = external {}

@experimental
NextTab<public>:input_action(logic) = external {}

@experimental
PreviousTab<public>:input_action(logic) = external {}

@experimental
NextPage<public>:input_action(logic) = external {}

@experimental
PreviousPage<public>:input_action(logic) = external {}
```

#### Inventory Menu

```verse
@experimental
InventoryMenuMapping<public>:input_mapping = external {}

@experimental
Use<public>:input_action(logic) = external {}

@experimental
Inspect<public>:input_action(logic) = external {}

@experimental
Sort<public>:input_action(logic) = external {}

@experimental
Drop<public>:input_action(logic) = external {}
```

#### Crafting Menu

```verse
@experimental
CraftingMenuMapping<public>:input_mapping = external {}

@experimental
Craft<public>:input_action(logic) = external {}

@experimental
Favorite<public>:input_action(logic) = external {}

@experimental
Scrap<public>:input_action(logic) = external {}
```

#### Map Menu

```verse
@experimental
MapMenuMapping<public>:input_mapping = external {}

@experimental
Track<public>:input_action(logic) = external {}

@experimental
Reset<public>:input_action(logic) = external {}

@experimental
PlaceMarker<public>:input_action(logic) = external {}

@experimental
ToggleView<public>:input_action(logic) = external {}

@experimental
ZoomIn<public>:input_action(logic) = external {}

@experimental
ZoomOut<public>:input_action(logic) = external {}
```

---

## BasicShapes Module

Module import path: `/UnrealEngine.com/BasicShapes`

```verse
BasicShapes<public> := module:
    using {/Verse.org/SceneGraph}

    cube<public> := class<final><public>(mesh_component):
    sphere<public> := class<final><public>(mesh_component):
    plane<public> := class<final><public>(mesh_component):
    cone<public> := class<final><public>(mesh_component):
    cylinder<public> := class<final><public>(mesh_component):
```

---

## Assets Module

Module import path: `/UnrealEngine.com/Assets`

```verse
(/UnrealEngine.com:)Assets<public> := module:
    using {/Verse.org/SpatialMath}
    using {/UnrealEngine.com/Temporary/SpatialMath}
    using {/Verse.org/Assets}

    SpawnParticleSystem<native><public>(Asset:particle_system, Position:(/UnrealEngine.com/Temporary/SpatialMath:)vector3, ?Rotation:(/UnrealEngine.com/Temporary/SpatialMath:)rotation, ?StartDelay:float)<transacts>:cancelable

    SpawnParticleSystem<native><public>(Asset:particle_system, Position:(/Verse.org/SpatialMath:)vector3, ?Rotation:(/Verse.org/SpatialMath:)rotation, ?StartDelay:float)<transacts>:cancelable
```
