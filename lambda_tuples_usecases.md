# Real World Use Cases: Lambda and Tuples

Easy examples you can relate to everyday life. No theory dump — just *when* and *why* people actually use these.

---

## Part 1: Lambda

A **lambda** is a tiny one-line function with no name.

Think of it like a sticky note: you write a small instruction, use it once, and throw it away. You do **not** need a full recipe (a `def` function) for something this small.

```python
# A normal function
def add(x, y):
    return x + y

# The same thing as a lambda
add = lambda x, y: x + y
```

### 1. Sorting a list of students by marks

You have student records and want the highest scorer first. Lambda tells `sort` *what* to look at.

```python
students = [
    {"name": "Akash", "marks": 72},
    {"name": "Ananya", "marks": 91},
    {"name": "Abhishek", "marks": 84},
]

students.sort(key=lambda student: student["marks"], reverse=True)
# Ananya (91), Abhishek (84), Akash (72)
```

**Real world:** leaderboards, exam results, "top products" on a shopping app.

### 2. Filtering a food delivery cart

Keep only items that cost less than ₹200.

```python
cart = [
    {"item": "Biryani", "price": 280},
    {"item": "Samosa", "price": 40},
    {"item": "Lassi", "price": 80},
]

cheap_items = list(filter(lambda food: food["price"] < 200, cart))
# Samosa, Lassi
```

**Real world:** "Show me only budget products", "Hide sold-out tickets", "Keep only unread emails".

### 3. Applying a discount to every item

`map` + lambda = do the same small change to every item.

```python
prices = [280, 40, 80]
discounted = list(map(lambda price: price * 0.9, prices))
# 10% off → [252.0, 36.0, 72.0]
```

**Real world:** GST calculation, converting Celsius to Fahrenheit, adding a service fee.

### 4. Quick button / callback logic

In apps, buttons often need a tiny action: "when clicked, do this". Lambda is perfect for that short action.

```python
# Imagine a "Pay" button
on_pay = lambda amount: print(f"Paid ₹{amount}")

on_pay(499)
```

**Real world:** UI buttons, timers ("after 5 seconds, close the popup"), event handlers.

### 5. Finding the cheapest / most expensive thing

```python
products = [
    ("Pen", 10),
    ("Notebook", 60),
    ("Bag", 799),
]

cheapest = min(products, key=lambda product: product[1])
# ("Pen", 10)
```

**Real world:** cheapest flight, nearest restaurant, oldest message in a chat.

---

## Part 2: Tuples

A **tuple** looks like a list, but once created it **cannot be changed**.

```python
my_list = [1, 2, 3]      # can change
my_tuple = (1, 2, 3)     # cannot change
```

Use a tuple when the values belong together **as one unit** and should stay that way — like a locked pair.

### 1. A location on a map (latitude, longitude)

A place has two numbers that always travel together. You should not accidentally change only one of them.

```python
home = (12.9716, 77.5946)   # Bengaluru
office = (28.6139, 77.2090) # Delhi
```

**Real world:** GPS pins, "share my location", delivery drop points.

### 2. RGB color of a pixel

Every color is a fixed mix of Red, Green, Blue. That mix should not be edited by mistake.

```python
white = (255, 255, 255)
black = (0, 0, 0)
airtribe_blue = (30, 144, 255)
```

**Real world:** image editing, website themes, "this brand color must stay the same".

### 3. Returning more than one value from a function

A function can hand back a pack of results at once.

```python
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return (quotient, remainder)

q, r = divide(17, 5)
# q = 3, r = 2
```

**Real world:** "give me name and age", "give me status and message", ATM returning (notes_count, leftover_amount).

### 4. Dictionary keys that need two pieces

A dictionary key must be unchangeable. A tuple works; a list does not.

```python
# Seat booking: (row, seat_number) → passenger name
seats = {
    ("A", 12): "Akash",
    ("B", 3): "Ananya",
    ("C", 7): "Abhishek",
}

print(seats[("B", 3)])  # Ananya
```

**Real world:** movie tickets, train berths, classroom roll (class, roll_no), chess board squares.

### 5. Days of the week / fixed options

Some collections should never grow or shrink.

```python
days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
# Nobody should be able to add an 8th day
```

**Real world:** months of the year, traffic-light colors, card suits (hearts, diamonds, clubs, spades).

---

## Lambda + Tuple together

These two show up together a lot.

### Sort people by age, then by name

Each person is a tuple: `(name, age)`.

```python
people = [
    ("Akash", 24),
    ("Ananya", 22),
    ("Abhishek", 24),
]

# First by age, if age is same then by name
people.sort(key=lambda person: (person[1], person[0]))
# Ananya 22, Abhishek 24, Akash 24
```

The lambda returns a **tuple**. Python sorts by the first item, then the second. That is how "sort by age, then name" works.

### Unpack a tuple inside a lambda

```python
scores = [("Akash", 72), ("Ananya", 91), ("Abhishek", 84)]

names = list(map(lambda student: student[0], scores))
# ["Akash", "Ananya", "Abhishek"]
```

---

## Quick cheat sheet

| Use this | When |
|---|---|
| **Lambda** | You need a tiny function for `sort`, `filter`, `map`, or a button click |
| **Tuple** | Values belong together and should not change (location, color, pair of results) |
| **List** | You need to add, remove, or update items later |
| **Normal `def` function** | The logic is more than one line, or you will reuse it many times |

**Rule of thumb**

- Sticky-note logic → **lambda**
- Locked pair / group → **tuple**
- Shopping bag you keep changing → **list**
