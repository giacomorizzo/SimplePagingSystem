package com.giacomorizzo.simplepagingsystemclient.adapters;

import java.util.List;
import com.giacomorizzo.simplepagingsystemclient.R;
import com.giacomorizzo.simplepagingsystemclient.beans.Notification;
import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;
 
public class NotificationsAdapter extends ArrayAdapter<Notification> {
 
    Context context;
 
    public NotificationsAdapter(Context context, int resourceId, List<Notification> items) {
        super(context, resourceId, items);
        this.context = context;
    }
 
    /*private view holder class*/
    private class ViewHolder {
        TextView txtMessage;
        TextView txtRequester;
		TextView txtReceiver;
    }
 
    public View getView(int position, View convertView, ViewGroup parent) {
        ViewHolder holder = null;
        Notification notification = getItem(position);
 
        LayoutInflater mInflater = (LayoutInflater) context
                .getSystemService(Activity.LAYOUT_INFLATER_SERVICE);
        if (convertView == null) {
            convertView = mInflater.inflate(R.layout.list_item, null);
            holder = new ViewHolder();
            holder.txtMessage = (TextView) convertView.findViewById(R.id.message);
            holder.txtRequester = (TextView) convertView.findViewById(R.id.requester);
            holder.txtReceiver = (TextView) convertView.findViewById(R.id.receiver);
            convertView.setTag(holder);
        } else
            holder = (ViewHolder) convertView.getTag();
 
        holder.txtMessage.setText(notification.getMessage());
        holder.txtRequester.setText(notification.getRequester());
        holder.txtReceiver.setText(notification.getReceiver());
 
        return convertView;
    }
}