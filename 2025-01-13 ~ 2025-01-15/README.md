# Stable Diffusion  
Azure Machine learning 생성  
computing instance 만들기(GPU)  

ssh -i <YOUR_PRIVATE_KEY_PATH> azureuser@<PUBLIC_IP_ADDRESS> -p 50000  
Are you sure you want to continue connecting (yes/no/[fingerprint])?  
yes  

git clone https://github.com/lllyasviel/stable-diffusion-webui-forge.git  
cd stable-diffusion-webui-forge  
conda create -n webui-forge python=3.10  
conda activate webui-forge  
cd ~/stable-diffusion-webui-forge/models/Stable-diffusion  

curl -H "Authorization: Bearer <HUGGINGFACE_TOKEN>" https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt --location --output v1-5-pruned-emaonly.ckpt  

curl -H "Authorization: Bearer <HUGGINGFACE_TOKEN>" https://huggingface.co/lllyasviel/flux1_dev/resolve/main/flux1-dev-fp8.safetensors --location --output sd_xl_base_1.0.safetensors  

curl -H "Authorization: Bearer <HUGGINGFACE_TOKEN>" https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors --location --output ae.safetensors  

curl -H "Authorization: Bearer <HUGGINGFACE_TOKEN>" https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors --location --output clip_l.safetensors  

mv sd_xl_base_1.0.safetensors flux1-dev-fp8.safetensors  
mv ae.safetensors ../VAE  
mv clip_l.safetensors ../text_encoder  

sudo apt-get update  
sudo apt-get install libgoogle-perftools-dev -y  
pip install civitdl  
sudo apt-get install lynx w3m links -y  

cd ../../  
./webui.sh --share --enable-insecure-extension-access --gradio-auth <username:password>  

Lora 모델  
https://civitai.com/  
~/stable-diffusion-webui-forge/models/Lora  
civitdl model_id . -k  

cd ~/stable-diffusion-webui-forge/outputs/txt2img-images/<YYYYMM_DD>  
zip -r output.zip .  
exit;  
scp -i "<YOUR_PRIVATE_KEY_PATH>" -P 50000 azureuser@<PUBLIC_IP_ADDRESS>:":/home/azureuser/stable-diffusion-webui-forge/outputs/txt2img-images/<YYYY-MM-DD>/output.zip" "<YOUR_DOWNLOAD_PATH>"  