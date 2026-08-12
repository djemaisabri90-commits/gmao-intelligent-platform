from maintenance.selectors.dashboard_selectors import get_dashboard_stats


def build_dashboard_data():

    data = get_dashboard_stats()

    machines_total = data["machines_total"]
    machines_down = data["machines_down"]

    availability = 0
    if machines_total > 0:
        availability = round(
            ((machines_total - machines_down) / machines_total) * 100, 2
        )

    return {
        "kpi": {
            "machines_total": machines_total,
            "machines_down": machines_down,
            "workorders_open": len(data["workorders_open"]),
            "interventions_running": len(data["interventions_running"]),
            "availability_percent": availability
        },
        "recent_interventions": [
            {
                "id": i.id,
                "machine": i.workorder.machine.nom,
                "technicien": i.technicien.user.username,
                "date_debut": i.date_debut
            }
            for i in data["recent_interventions"]
        ],
        "recent_logs": [
            {
                "machine": log.machine.nom,
                "action": log.action,
                "date": log.date
            }
            for log in data["recent_logs"]
        ],
        "machines_most_failures": [
            {
                "machine": m.nom,
                "pannes": m.total_workorders
            }
            for m in data["machines_most_failures"]
        ]
    }