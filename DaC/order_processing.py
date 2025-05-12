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
        with Cluster("Data Input"):
            Wto = Audit("Weiter Takes Order")
        
        with Cluster("Order Handling"):
            db_in = Backbone("Entry To The Database")
            kv = Notifications("New Order In Kitchen Display")
            or_ga = Alarm("Order Giveaway")
            ch_state = ELB("Change Order State")
            db_reg = Tagging("Locked Ingredients")
            
        with Cluster("Final Transaction"):
            order_sum = Buckets("Generate Order Summary")
            op_dis = IDAccess("Optional Discount")
            status = DataTransfer("Set status to 'Completed'")
            
        Wto >> db_in
        db_in >> kv
        kv >> or_ga
        or_ga >> ch_state
        db_in >> db_reg

        or_ga >> order_sum
        order_sum >> op_dis
        op_dis >> status
