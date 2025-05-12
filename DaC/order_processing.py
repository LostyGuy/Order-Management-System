from diagrams import Cluster, Diagram

# AWS Icons
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53

# OCI Icons
from diagrams.oci.governance import Audit
from diagrams.oci.governance import Tagging
from diagrams.oci.connectivity import Backbone
from diagrams.oci.monitoring import Notifications
from diagrams.oci.monitoring import Alarm
from diagrams.oci.storage import Buckets
from diagrams.oci.storage import DataTransfer
from diagrams.oci.security import IDAccess


with Diagram("Order Processing", show=False, filename="RDME_files/order_processing", outformat="png", node_attr={"fontsize": "10", "fontname": "bold"}):
    with Cluster(""):
        with Cluster("Data Input", graph_attr={"fontsize": "12","fontname": "bold"}):
            Wto = Audit("Weiter Takes Order")
        
        with Cluster("Order Handling", graph_attr={"fontsize": "12","fontname": "bold"}):
            db_in = Backbone("Entry To\n The Database")
            kv = Notifications("New Order\n In Kitchen Display")
            or_ga = Alarm("Order Giveaway")
            ch_state = Backbone("Change Order State\n (Given Away)")
            db_reg = Tagging("Locked Ingredients")
            rm_kv_order = Notifications("Remove Order\n From Kitchen Display")
            
        with Cluster("Final Transaction", graph_attr={"fontsize": "12","fontname": "bold"}):
            order_sum = Buckets("Generate Order\n Summary")
            op_dis = IDAccess("Optional Discount")
            status = DataTransfer("Set status\n to 'Completed'")
            
        Wto >> db_in
        db_in >> kv
        kv >> or_ga
        or_ga >> ch_state
        ch_state >> rm_kv_order
        db_in >> db_reg

        ch_state >> order_sum
        order_sum >> op_dis
        op_dis >> status
