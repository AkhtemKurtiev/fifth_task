from test.unit.conftest import TestModelRepository


class TestRepository:
    async def test_simple_add_one(self, repository: TestModelRepository):
        await repository.add_one(name='Test1')
        result = await repository.get_by_query_one_or_none(name='Test1')
        assert result is not None
        assert result.name == 'Test1'

    async def test_add_one_and_get_id(self, repository: TestModelRepository):
        result_return = await repository.add_one_and_get_id(name='Test2')
        result = await repository.get_by_query_one_or_none(name='Test2')
        assert result is not None
        assert result.name == 'Test2'
        assert result_return == 2

    async def test_add_one_and_get_obj(self, repository: TestModelRepository):
        result_return = await repository.add_one_and_get_obj(name='Test3')
        result = await repository.get_by_query_one_or_none(name='Test3')
        assert result is not None
        assert result.name == 'Test3'
        assert result_return.name == 'Test3'

    async def test_get_by_query_one_or_none(
            self, repository: TestModelRepository
    ):
        await repository.add_one(name='Test4')
        result = await repository.get_by_query_one_or_none(name='Test4')
        assert result is not None
        assert result.name == 'Test4'

    async def test_get_by_query_all(self, repository: TestModelRepository):
        await repository.delete_all()
        await repository.add_one(name='Test5')
        await repository.add_one(name='Test55')
        results = await repository.get_by_query_all()
        assert len(results) == 2

    async def test_get_by_query_all_filter_between(
            self, repository: TestModelRepository
    ):
        await repository.add_one(name='TestFilter1')
        await repository.add_one(name='TestFilter2')
        await repository.add_one(name='TestFilter3')
        await repository.add_one(name='TestFilter4')
        results = await repository.get_by_query_all(
            name=('TestFilter1', 'TestFilter3')
        )
        assert len(results) == 3

    async def test_update_one_by_id(self, repository: TestModelRepository):
        obj = await repository.add_one_and_get_obj(name='Test6')
        result = await repository.update_one_by_id(obj.id, {'name': 'Test66'})
        assert result is not None
        assert result.name == 'Test66'

    async def test_delete_by_query(self, repository: TestModelRepository):
        await repository.add_one(name='Test7')
        await repository.delete_by_query(name='Test7')
        result = await repository.get_by_query_one_or_none(name='Test7')
        assert result is None

    async def test_delete_all(self, repository: TestModelRepository):
        await repository.add_one(name='Test8')
        await repository.add_one(name='Test88')
        await repository.delete_all()
        result1 = await repository.get_by_query_one_or_none(name='Test8')
        result2 = await repository.get_by_query_one_or_none(name='Test88')
        assert result1 is None
        assert result2 is None
