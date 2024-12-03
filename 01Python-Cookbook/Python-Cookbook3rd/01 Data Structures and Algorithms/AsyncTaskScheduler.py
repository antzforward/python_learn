"""
在实现异步任务调度时，使用优先队列仍然是一种有效的方法，尤其是当需要根据某些标准（如优先级）来决定任务执行顺序时。优先队列能帮助调度器从多个待处理的任务中快速选出下一个应执行的任务。

异步任务调度与优先队列
在异步编程中，任务通常指一段需要被执行但不会立即完成的代码，这可能包括IO操作、网络请求等。调度器的角色是管理何时以及如何执行这些任务。

为什么使用优先队列：

优先级管理： 优先队列允许你根据任务的优先级进行排序，确保高优先级任务先执行。
效率： 使用优先队列可以高效地插入新任务和取出当前最紧急的任务，通常的操作时间复杂度为 O(log n)。

注意事项
异常处理: 确保捕获并适当处理异步任务中的异常，避免某个任务的失败影响整个调度器。
并发控制: 考虑到并发，如果有大量的高优先级任务，可能需要维护它们的合理分布，避免低优先级任务饿死。
任务插入时机: 在高并发系统中，频繁的任务插入和提取可能会成为性能瓶颈，适当优化数据结构或使用批处理可以减轻这一问题。
使用优先队列来实现异步任务调度是一个强大而灵活的方案，能够满足多种调度需求。
"""
import asyncio
import heapq


class AsyncTaskScheduler:
    def __init__(self):
        self.tasks = []  # 用一个堆作为优先队列

    async def run(self):
        while self.tasks:
            priority, task = heapq.heappop(self.tasks)
            try:
                await task  # 运行任务
            except Exception as e:
                print(f"Task failed: {e}")

    def add_task(self, task, priority=0):
        heapq.heappush(self.tasks, (priority, task))  # 添加任务


# 示例用法
async def do_some_work(x):
    print(f"Working on {x}")
    await asyncio.sleep(1)  # 模拟异步操作
    print(f"Done {x}")


async def main():
    scheduler = AsyncTaskScheduler()
    scheduler.add_task(do_some_work("high priority task"), priority=-1)  # 高优先级任务
    scheduler.add_task(do_some_work("low priority task"))  # 默认优先级为 0
    await scheduler.run()


asyncio.run(main())