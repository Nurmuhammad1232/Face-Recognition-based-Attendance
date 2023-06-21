import pandas as pd
from postgres.postgres import get_workers


class Workers(pd.DataFrame):
    def __init__(self) -> None:
        workers = get_workers()
        # if not workers.empty:
        #     workers['leave_time'] = workers['leave_time'].astype(str).str[:-3]
        #     workers['come_time'] = workers['come_time'].astype(str).str[:-3]
        # workers['come_time']

        super().__init__(workers.to_dict())
