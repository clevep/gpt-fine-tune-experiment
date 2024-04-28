import fine_tune

# file_id = fine_tune.upload_file()
# fine_tune.create_fine_tune_job(file_id)

fine_tuned_model_name = "ft:gpt-3.5-turbo-0613:personal::9J5EJuL3"
system_prompt = "Marv is a factual chatbot that is also sarcastic."
user_prompt = "Who was George Washington"
fine_tune.query_fine_tune_model(fine_tuned_model_name, system_prompt=system_prompt, user_prompt=user_prompt)