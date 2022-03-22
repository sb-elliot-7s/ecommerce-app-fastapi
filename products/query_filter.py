from sqlalchemy import between, Column


class QueryService:

    async def price_compare(self, stmt, price_data: dict, column: Column):
        min_price = price_data.get('min_price')
        max_price = price_data.get('max_price')
        if price_data:
            expr = await self._compare(column=column, left=min_price, right=max_price)
            return stmt.where(expr)
        return stmt

    @staticmethod
    async def _compare(left, right, column: Column):
        return between(column, lower_bound=left, upper_bound=right) if left and right \
            else column >= left if not right \
            else column <= right if not left else None

    @staticmethod
    async def filtered(stmt, data: dict, key: str, column: Column):
        value = data.get(key)
        if not value:
            return stmt
        if len(value) > 1:
            return stmt.where(column.in_(value))
        return stmt.where(column == value[0])


