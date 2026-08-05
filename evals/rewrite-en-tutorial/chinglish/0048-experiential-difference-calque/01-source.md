**`session.scalars(select(Book))`** 返回的是 `Book` 实例的迭代器, 你拿到的不是 row tuple 而是有方法、有属性的 Python 对象, 这是 ORM 跟 Core 最大的体感差别。
