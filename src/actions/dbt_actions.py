from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import os

class ActionQueryDbtMetadata(Action):
    def name(self) -> Text:
        return "action_query_dbt_metadata"

    def load_metadata(self) -> Dict:
        metadata_path = os.path.join('chatdbt_raw_data', 'dbt_metadata.json')
        with open(metadata_path, 'r') as f:
            return json.load(f)

    def execute(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message
        user_message = tracker.latest_message.get('text', '')
        
        try:
            metadata = self.load_metadata()
            
            # Extract intent and entities from the tracker
            intent = tracker.latest_message['intent'].get('name')
            entities = tracker.latest_message.get('entities', [])

            # Handle different types of queries
            if intent == "query_model_description":
                model_name = next((e['value'] for e in entities if e['entity'] == 'model_name'), None)
                if model_name:
                    model = next((m for m in metadata['models'] if m['name'] == model_name), None)
                    if model:
                        response = f"Model {model_name}: {model['description']}"
                    else:
                        response = f"Model {model_name} not found."
                else:
                    response = "Please specify a model name."

            elif intent == "query_column_info":
                model_name = next((e['value'] for e in entities if e['entity'] == 'model_name'), None)
                column_name = next((e['value'] for e in entities if e['entity'] == 'column_name'), None)
                
                if model_name and column_name:
                    model = next((m for m in metadata['models'] if m['name'] == model_name), None)
                    if model:
                        column = next((c for c in model['columns'] if c['name'] == column_name), None)
                        if column:
                            response = f"Column {column_name} in {model_name}: {column.get('description', 'No description available')}"
                        else:
                            response = f"Column {column_name} not found in model {model_name}."
                    else:
                        response = f"Model {model_name} not found."
                else:
                    response = "Please specify both model and column names."

            elif intent == "query_relationships":
                model_name = next((e['value'] for e in entities if e['entity'] == 'model_name'), None)
                if model_name:
                    relationships = [r for r in metadata['relationships'] 
                                   if r['from_model'] == model_name or r['to_model'] == model_name]
                    if relationships:
                        response = f"Relationships for {model_name}:\n"
                        for r in relationships:
                            response += f"- {r['from_model']}.{r['from_column']} → {r['to_model']}.{r['to_column']}\n"
                    else:
                        response = f"No relationships found for model {model_name}."
                else:
                    response = "Please specify a model name."

            else:
                response = "I'm not sure how to handle that query. You can ask about model descriptions, column information, or relationships."

            dispatcher.utter_message(text=response)

        except Exception as e:
            dispatcher.utter_message(text=f"Error processing request: {str(e)}")

        return [] 