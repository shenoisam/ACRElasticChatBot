# Elastic ACR Criteria
## Project Description

## Authors
- Sam Shenoi

## Set up
1. Clone this repo and navigate to the folder in terminal
    - Be sure to read the following articles to learn how to do this if you haven't before.
        - https://medium.com/codex/introduction-to-bash-for-biomedical-research-part-1-3-cf7b512ade2a
        - https://medium.com/codex/introduction-to-bash-for-biomedical-research-part-2-3-62daa725fe53
        - https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
2. Install virtualenv and create a new virtualenv
```
pip3 install virtualenv
virtualenv venv
source venv bin activate
```
   - Read about virtualenvs here: https://sourabhbajaj.com/mac-setup/Python/virtualenv.html

3. Install dependencies
`pip3 install -r requirements.txt`

4. Set up elasticsearch. Refer to this article (https://medium.com/@bananachiptech/how-to-set-up-a-elasticsearch-on-mac-f21a2c9d0b1f)

5. Download the data from (https://docs.google.com/document/d/13ZvdI1auJl3UN16kHwm-wS08MjWEGlI4DCN3dRx81FM/edit?usp=share_link). Be sure to download it as a txt file and copy it into this folder. We named it out.txt.

6. Run the following command to load the data into elasticsearch. Make sure that your elastic search instance is running!
```
python3 main.py --load_data out.txt
```

7. Now you can run the program! Use the following command to run.
`python3 main.py`
You can provide different prompts to the program by running the following command in your terminal
`python3 main.py --prompt "<your prompt here>"`