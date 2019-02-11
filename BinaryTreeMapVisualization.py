#!/usr/bin/env python
import BinarySearchTreeMap
import math
import turtle
import time

canvas = turtle.Turtle()

screen_width = canvas.screen.window_width()
screen_height = canvas.screen.window_height()
canvas.screen.setworldcoordinates(0, 0, screen_width, screen_height)

start_x = 0
start_y = screen_height

canvas.speed(0)
canvas.penup()
canvas.goto(start_x, start_y)
canvas.pendown()

# Set tracer to False to remove animations
turtle.Screen().tracer(True)

def main():

    height_of_tree = 5
    size_of_tree = math.pow(2, height_of_tree) - 1

    leftmost_key = 100
    rightmost_key = leftmost_key + size_of_tree

    bst = create_complete_bst_helper(leftmost_key, rightmost_key)

    draw_tree_recursive(bst, 20)
    time.sleep(2)
    canvas.clear()

    # Sample: delete the minimum node, draw tree (until tree is of size 10)
    for i in range(bst.size - 10):
        del bst[leftmost_key + i]
        draw_tree_recursive(bst, 20)
        time.sleep(2.0)
        canvas.clear()

    turtle.done()

    pass


def draw_node(x, y, node=None, radius=5, fill=True):
    canvas.penup()
    if (fill):
        canvas.goto(x, y)
        canvas.pendown()
        canvas.dot(radius * 2)
    else:

        # Assume height ~= width, then radius = height ~= width
        if (node is not None):
            word_width = radius * len(str(node.item.key))
            canvas.goto(x - word_width // 4, y - radius // 2)
            canvas.pendown()
            canvas.write(node.item.key, font=("Arial", radius, "normal"))
            canvas.penup()

        canvas.goto(x, y - radius)
        canvas.pendown()
        canvas.circle(radius)
        canvas.penup()
        canvas.goto(x, y)
        canvas.pendown()

    pass


def draw_subtree(subtree_root, node_radius=10):
    new_tree = BinarySearchTreeMap.BinarySearchTreeMap(subtree_root)
    draw_tree_recursive(new_tree, node_radius)

def draw_tree_recursive(bst, node_radius=10, bound_left=10, bound_right=screen_width - 10, y_pos=screen_height - 80):
    if (bst.is_empty()):
        raise Exception("Tree is empty")
    # Height should be redefined as distance from deepest node in tree (deepest node will be 0 from itself)
    amount_of_levels = float(bst.root.height - (1 if bst.root.height > 1 else 0))
    y_step = ((screen_height - 160) / amount_of_levels)
    draw_tree_recursive_helper(bst, node_radius, bst.root, bound_left, bound_right, y_pos, y_step)


def draw_tree_recursive_helper(bst, node_radius, root, bound_left, bound_right, y_pos, y_step):

    if (root is not None):
        # When calling on children, connect entire subtree rooted at each child
        # What's left is to connect current node to parent

        root_x = (bound_left + bound_right) // 2

        # Drawing current subtree root
        draw_node(root_x, y_pos, root, node_radius, False)

        # Draw lines from root to parent
        # Use pythagorean theorem for distance and inverse trig function for angle (based on ratio|slope)
        if (root.parent is not None):

            delta_y = y_step

            # Based on testing with turtle, left angle shift actually maps to left child
            # delta_x is x offset from parent to root
            # delta_y is y offset from parent to root
            if (root is root.parent.left):

                delta_x = root_x + (bound_right - root_x * 2)
                distance = math.sqrt(math.pow(delta_y, 2) + math.pow(delta_x, 2))

                try:
                    angle = math.atan(float(delta_y) / float(delta_x)) * (180 / math.pi)
                except ZeroDivisionError as zde:
                    angle = 90

                # distance_in_circle is distance to travel, before drawing line, to avoid drawing line
                # -within a node
                distance_in_circle = node_radius

                canvas.left(angle)

                canvas.penup()
                canvas.forward(node_radius)
                canvas.pendown()

                canvas.forward(distance - node_radius * 2)
                canvas.right(angle)

                canvas.penup()
                canvas.forward(node_radius)
                canvas.pendown()

            else:  # root is root.parent.right

                delta_x = root_x - bound_left
                distance = math.sqrt(math.pow(delta_y, 2) + math.pow(delta_x, 2))

                try:
                    angle = math.atan(float(delta_y) / float(delta_x)) * (180 / math.pi)
                except ZeroDivisionError as zde:
                    angle = 90

                canvas.left(180 - angle)

                canvas.penup()
                canvas.forward(node_radius)
                canvas.pendown()

                canvas.forward(distance - node_radius * 2)
                canvas.right(180 - angle)
                pass

        # Drawing subtrees
        draw_tree_recursive_helper(bst, node_radius, root.left, bound_left, root_x, y_pos - y_step, y_step)
        # if (root is not bst.root):
        draw_tree_recursive_helper(bst, node_radius, root.right, root_x, bound_right, y_pos - y_step, y_step)

    pass


def is_balanced(bst):
    return is_balanced_helper(bst.root)[0]


def is_balanced_helper(root):
    # Output: (balance_state, height)
    if (root is None):
        return (True, 0)
    else:
        # When calling on children, return height of both children and whether or not each is balanced
        # What's left is to continue if height difference <= 1 && if both are balanced

        pair_left = is_balanced_helper(root.left)
        pair_right = is_balanced_helper(root.right)

        children_both_balanced = pair_left[0] and pair_right[0]
        child_height_difference = abs(pair_left[1] - pair_right[1])

        height_curr = max(pair_left[1], pair_right[1]) + 1

        return (children_both_balanced and child_height_difference <= 1, height_curr)


def create_complete_bst(first_to_end):
    return create_complete_bst_helper(1, first_to_end)


def create_complete_bst_helper(first_to_start, first_to_end):
    bst = BinarySearchTreeMap.BinarySearchTreeMap()
    add_items(bst, first_to_start, first_to_end)
    return bst


def add_items(bst, low, high):

    if (low < high):

        # When calling on range from low to mid, and mid to high, insert all nodes < mid and > mid to tree
        # What's left is to insert the middle node as the root, or insert before children

        # Current node is the middle node
        mid = int((low + high) // 2)

        bst[mid] = None
        add_items(bst, low, mid)
        add_items(bst, mid + 1, high)

main()
