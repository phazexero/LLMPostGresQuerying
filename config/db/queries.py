# db/queries/queries.py

GROUP_QUERY = """
SELECT g.name FROM groups g WHERE g.organization_id = :org_id ORDER BY g.group_id;
"""

GET_LEDGER_QUERY = """
            select l.name as ledger_name, g.name as group_name
            from ledgers l, groups g
            where l.organization_id =g.organization_id and l.group_id =g.group_id 
            and l.organization_id = :org_id
            order by l.name;
"""
