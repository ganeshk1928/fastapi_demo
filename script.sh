if [[ $# -eq 6 ]]; then
  export TEAM=$1
  export ENVIRONMENT=$2
  export EKS_VERSION=$3
  export CLUSTER_NAME=$4
  export TERRAFORM_VERSION=$5
  export TFVARS_URL=$6
else
  echo "Inusfficient data"
  exit 1
fi

echo "Team name - $TEAM"
echo "Cluster Environment - $ENVIRONMENT"
echo "AWS EKS Version - $EKS_VERSION"
echo "Cluster Name - $CLUSTER_NAME"
echo "Terraform Version - $TERRAFORM_VERSION"
echo "Terraform variable files url - $TFVARS_URL"