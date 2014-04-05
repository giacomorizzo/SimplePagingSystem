package com.giacomorizzo.simplepagingsystemclient.activities;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.Credentials;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.giacomorizzo.simplepagingsystemclient.R;
import com.giacomorizzo.simplepagingsystemclient.adapters.NotificationsAdapter;
import com.giacomorizzo.simplepagingsystemclient.beans.Notification;

import android.annotation.TargetApi;
import android.app.ListActivity;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Toast;


@TargetApi(Build.VERSION_CODES.KITKAT)
public class MainActivity extends ListActivity implements OnItemClickListener {
    ListView listView;
    List<Notification> notifications;
    NotificationsAdapter listview_adapter;

    /** API basic settings (version and URI).
     * TODO: move to HTTPS in production
     */
    String api_endpoint = "http://10.0.0.1:5000";
    String api_version = "/v0.1";
        
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
  
        listView = getListView();

        notifications = getAvailableNotifications();
        
        listview_adapter = new NotificationsAdapter(this, R.layout.list_item, notifications);
        listView.setAdapter(listview_adapter);
        
        listView.setOnItemClickListener(this);  
    
	    final Handler handler = new Handler();
	    handler.postDelayed( new Runnable() {
	
	        @Override
	        public void run() {       	
	        	notifications = getAvailableNotifications();
	        	listview_adapter.clear();
	        	listview_adapter.addAll(notifications);
	        	listview_adapter.notifyDataSetChanged();
	            
	            handler.postDelayed( this, 3000 );
	        }
	    }, 3000 );
    }    
    
    private String api_request(String api_call) {
        String urlString = api_endpoint + api_version + api_call;
        
		try {
			return new HttpAsyncTask().execute(urlString).get();
		} catch (InterruptedException e) {
			System.out.println("An InterruptionException occurred during a remote REST API call");
			System.out.println("Request:" + urlString);
			e.printStackTrace();
		} catch (ExecutionException e) {
			System.out.println("An ExecutionException occurred during a remote REST API call");
			System.out.println("Request:" + urlString);
			e.printStackTrace();
		}
		return null;
    }
    
	private List<Notification> getAvailableNotifications() {
    	List<Notification> api_notifications = new ArrayList<Notification>();
        JSONArray api_result = null;
        String request = "/getAvailableNotifications";
        
		try {
			String object = api_request(request);
			api_result = new JSONArray(object);
		} catch (JSONException e) {
			System.out.println("A JSONException occurred while parsing api_result JSON");
			System.out.println("Request:" + request);
			e.printStackTrace();
		}
        
		for (int i = 0; i < api_result.length(); i++) {
			try {
				JSONObject item = api_result.getJSONObject(i);
				Notification notif = new Notification(
						item.getString("message"),
						item.getString("requester"),
						item.getString("receiver"),
						item.getString("id"),
						item.getString("status")
						);
				
				api_notifications.add(notif);
			} catch (JSONException e) {
				System.out.println("A JSONException occurred while parsing an element of the api_result JSON");
				System.out.println("Item nr:" + i);
				e.printStackTrace();
			}
        }
        return api_notifications;

    }
    
    private void acknowledgeNotification(Notification notification) {
        String api_call = "/acknowledgeNotification/" + notification.getId();
        api_request(api_call);

    	Toast toast = Toast.makeText(getApplicationContext(), "Acknwoledged", Toast.LENGTH_SHORT);
    	toast.setGravity(Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL, 0, 0);
    	toast.show();
    	
    	notifications.remove(notification);
    	listview_adapter.notifyDataSetChanged();
    }

    /** Parameters:
    adapter - The AdapterView where the click happened.
    view - The view within the AdapterView that was clicked
    position - The position of the view in the adapter.
    id - The row id of the item that was clicked.
     */
    @Override
    public void onItemClick(AdapterView<?> adapter, View view, int position, long id) {
    	acknowledgeNotification(notifications.get(position));
    }

	@Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
        
    private class HttpAsyncTask extends AsyncTask<String, Void, String> {
        
		protected String doInBackground(String... urls) {
	    	StringBuilder builder = new StringBuilder();
		    HttpClient httpClient = new DefaultHttpClient();
		    HttpGet httpGet = new HttpGet(urls[0]);
		    
		    httpGet.addHeader(BasicScheme.authenticate(new UsernamePasswordCredentials("username", "password"), "UTF-8", false));
/*		    Credentials defaultcreds = new UsernamePasswordCredentials("username", "password");
		    httpClient.getCredentialsProvider().setCredentials(new AuthScope("10.0.0.1", AuthScope.ANY_PORT), defaultcreds);*/
		    
		    try {
		    	HttpResponse response = httpClient.execute(httpGet);
	    		HttpEntity entity = response.getEntity();
	    		InputStream content = entity.getContent();
	    		BufferedReader reader = new BufferedReader(new InputStreamReader(content));
	    		String line;
	    		
	    		while ((line = reader.readLine()) != null) {
	    			builder.append(line);
	    		}
	    		
		    } catch (ClientProtocolException e) {
		    	e.printStackTrace();
		    } catch (IOException e) {
		    	e.printStackTrace();
		    }
		    return builder.toString();

        }
		
        // onPostExecute displays the results of the AsyncTask.
        protected void onPostExecute(String result) {
            //Toast.makeText(getBaseContext(), "Received!", Toast.LENGTH_LONG).show();
       }
    }    
}
