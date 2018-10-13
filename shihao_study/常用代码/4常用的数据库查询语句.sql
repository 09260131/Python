1. 添加联合索引
CREATE INDEX index1 ON host_hours_amount (`resource_id`, `commodity`, `consume_type`);