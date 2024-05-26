To create a PostgreSQL 14.5 resource in Kubernetes, you can use a Helm chart, which simplifies the process of deploying and managing applications on Kubernetes. Here’s a step-by-step guide using the Bitnami PostgreSQL Helm chart:

1. **Add the Bitnami Helm repository:**

   ```sh
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```

2. **Create a values file for customization:**

   Create a `values.yaml` file to specify PostgreSQL version and any other custom configurations you need. Here is an example of a `values.yaml` file for PostgreSQL 14.5:

   ```yaml
   image:
     registry: docker.io
     repository: bitnami/postgresql
     tag: 14.5.0-debian-10-r0

   global:
     postgresql:
       auth:
         postgresPassword: mypassword
         username: myuser
         password: mypassword
         database: mydatabase

   primary:
     persistence:
       enabled: true
       size: 8Gi
       storageClass: "standard" # Adjust based on your storage class
   ```

3. **Install the PostgreSQL chart with the custom values:**

   ```sh
   helm install my-postgresql -f values.yaml bitnami/postgresql
   ```

   This command installs the PostgreSQL chart using your custom `values.yaml` file.

4. **Verify the installation:**

   ```sh
   kubectl get pods
   ```

   Check that the PostgreSQL pod is running.

5. **Access PostgreSQL:**

   You can access your PostgreSQL instance using port forwarding:

   ```sh
   kubectl port-forward svc/my-postgresql 5432:5432
   ```

   Then, you can connect to it using any PostgreSQL client, such as `psql`:

   ```sh
   psql -h 127.0.0.1 -U myuser -d mydatabase
   ```

This setup uses the Bitnami PostgreSQL chart, which is a well-maintained and widely used Helm chart for deploying PostgreSQL on Kubernetes. Adjust the values in the `values.yaml` file as needed for your specific requirements.



#### just yaml

If you prefer to create a PostgreSQL 14.5 resource using just YAML files without Helm, you can define Kubernetes resources such as a PersistentVolume, PersistentVolumeClaim, Deployment, and Service. Below is an example of how to do this:

1. **PersistentVolume (optional if using dynamic provisioning):**

   ```yaml
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: postgres-pv
   spec:
     capacity:
       storage: 8Gi
     accessModes:
       - ReadWriteOnce
     persistentVolumeReclaimPolicy: Retain
     storageClassName: manual
     hostPath:
       path: "/mnt/data/postgres"
   ```

2. **PersistentVolumeClaim:**

   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: postgres-pvc
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 8Gi
     storageClassName: manual
   ```

3. **Deployment:**

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: postgres
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: postgres
     template:
       metadata:
         labels:
           app: postgres
       spec:
         containers:
         - name: postgres
           image: postgres:14.5
           ports:
           - containerPort: 5432
           env:
           - name: POSTGRES_DB
             value: "mydatabase"
           - name: POSTGRES_USER
             value: "myuser"
           - name: POSTGRES_PASSWORD
             value: "mypassword"
           volumeMounts:
           - mountPath: /var/lib/postgresql/data
             name: postgres-storage
         volumes:
         - name: postgres-storage
           persistentVolumeClaim:
             claimName: postgres-pvc
   ```

4. **Service:**

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: postgres
   spec:
     type: ClusterIP
     ports:
       - port: 5432
     selector:
       app: postgres
   ```

To apply these YAML files, save each block into separate files (e.g., `pv.yaml`, `pvc.yaml`, `deployment.yaml`, `service.yaml`), and then apply them using `kubectl`:

```sh
kubectl apply -f pv.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

This will set up a PostgreSQL 14.5 instance in your Kubernetes cluster. Adjust the configurations such as storage class, paths, and credentials as needed for your environment.