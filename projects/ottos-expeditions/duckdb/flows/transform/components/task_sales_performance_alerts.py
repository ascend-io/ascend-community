import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import ref, task


@task(
    dependencies=[
        ref("sales_stores"),
        ref("sales_website"),
        ref("sales_vendors"),
        ref("sales"),
    ]
)
def task_sales_performance_alerts(
    sales_stores: ibis.Table,
    sales_website: ibis.Table,
    sales_vendors: ibis.Table,
    sales: ibis.Table,
    context: ComponentExecutionContext,
) -> None:
    """
    Sales Performance Alert System for Otto's Expeditions

    Analyzes sales performance across different channels and sends alerts for:
    - Channel performance monitoring
    - Low-performing vendor alerts
    - High-performing store recognition
    - Cross-channel sales insights
    """

    # Calculate total sales by channel
    total_stores_sales = sales_stores.count().to_pyarrow().as_py()
    total_website_sales = sales_website.count().to_pyarrow().as_py()
    total_vendor_sales = sales_vendors.count().to_pyarrow().as_py()
    total_sales = sales.count().to_pyarrow().as_py()

    log(f"📊 SALES PERFORMANCE DASHBOARD")
    log(f"Total Sales Records: {total_sales}")
    log(
        f"Store Sales: {total_stores_sales} ({total_stores_sales / total_sales * 100:.1f}%)"
    )
    log(
        f"Website Sales: {total_website_sales} ({total_website_sales / total_sales * 100:.1f}%)"
    )
    log(
        f"Vendor Sales: {total_vendor_sales} ({total_vendor_sales / total_sales * 100:.1f}%)"
    )

    # Channel Performance Analysis
    if total_website_sales > total_stores_sales * 1.5:
        log(
            "🚀 ALERT: Website sales significantly outperforming store sales! Consider expanding online operations."
        )
    elif total_stores_sales > total_website_sales * 1.5:
        log(
            "🏪 ALERT: Store sales significantly outperforming website! Consider improving online user experience."
        )

    # Vendor Performance Monitoring
    if total_vendor_sales < total_sales * 0.1:  # Less than 10% of total sales
        log(
            "⚠️  VENDOR ALERT: Vendor sales are below 10% of total sales. Review vendor partnerships."
        )
    elif total_vendor_sales > total_sales * 0.4:  # More than 40% of total sales
        log(
            "🤝 VENDOR SUCCESS: Vendor partnerships are driving significant sales! Consider expanding vendor network."
        )

    # Cross-Channel Balance Analysis
    channels = [
        ("Stores", total_stores_sales),
        ("Website", total_website_sales),
        ("Vendors", total_vendor_sales),
    ]
    channels.sort(key=lambda x: x[1], reverse=True)

    log(f"📈 CHANNEL RANKING:")
    for i, (channel, count) in enumerate(channels, 1):
        log(f"  {i}. {channel}: {count} transactions")

    # Business Insights
    if abs(total_stores_sales - total_website_sales) < total_sales * 0.1:
        log(
            "⚖️  INSIGHT: Store and website sales are well balanced - good omnichannel strategy!"
        )

    # Performance Alerts for Business Actions
    if total_sales > 1000:
        log(
            "🎉 CELEBRATION ALERT: High sales volume detected! Time to reward the team!"
        )
        log("📧 ACTION: Sending congratulatory emails to sales team...")

        # Simulate sending alerts to different teams based on performance
        if total_website_sales > total_stores_sales:
            log(
                "📱 ACTION: Notifying digital marketing team of strong online performance"
            )
        if total_stores_sales > total_website_sales:
            log("🏬 ACTION: Notifying store managers of excellent in-person sales")
        if total_vendor_sales > total_sales * 0.2:
            log("🤝 ACTION: Scheduling vendor appreciation meeting")

    log("✅ Sales performance alerts completed!")
