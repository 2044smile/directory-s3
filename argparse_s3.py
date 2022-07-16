import os
import boto3
import argparse


BUCKET = os.getenv("BUCKET", "seller-car")
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

                           # /date/{2022-01-01}/sell/car 
                                            # seller-car
                                                    # /sell/car/mercedes_benz/
             # sell                                 # /sell/car/bmw/
def upload_dir(profile_name, local_directory, bucket, destination):
    if(False == os.path.isdir(local_directory)):
        return False

    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client('s3')

    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_directory)

            s3_path = f"{destination}/{filename}"

            try:
                print(f"Uploading {s3_path}")
                s3_client.upload_file(local_path, bucket, s3_path)
            except ClientError as e:
                print(e)
                return False

    return True


def sell_car(car_brand, car_input_path, car_output_path):
    if car_brand == "bmw":
        input_path = car_input_path
        output_path = car_output_path
        
        upload_dir("default", f"{input_path}", f"{BUCKET}", f"{output_path}")
    elif car_brand == "hyundai":
        input_path = car_input_path
        output_path = car_output_path
        
        upload_dir("default", f"{input_path}", f"{BUCKET}", f"{output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="if you choose")
    parser.add_argument('--car-brand', required=True, help="bmw or hyundai")
    parser.add_argument('--car-input-path', required=True, help="/date/2022-01-01/sell/car/hyundai/")
    parser.add_argument('--car-output-path', required=True, help="car/hyundai/")

    args = parser.parse_args()
    sell_car(args.car_brand, args.car_input_path, args.car_output_path)
