package com.giacomorizzo.simplepagingsystemclient.beans;

public class Notification {
	private String message;
	private String requester;
	private String receiver;
	private String id;
	private String status;
	
	//public Notification(String message, String requester, String receiver, int id, String status) {
	public Notification(String message, String requester, String receiver, String id, String status) {
		super();
		this.message = message;
		this.requester = requester;
		this.receiver = receiver;
		this.id = id;
		this.status = status;
	}
	
	/**
	 * @return the message
	 */
	public String getMessage() {
		return message;
	}
	/**
	 * @return the requester
	 */
	public String getRequester() {
		return requester;
	}
	/**
	 * @return the receiver
	 */
	public String getReceiver() {
		return receiver;
	} 
	/**
	 * @return the id
	 */
	public String getId() {
		return id;
	}
	/**
	 * @return the status
	 */
	public String getStatus() {
		return status;
	}
	
	@Override
    public String toString() {
        return "Message: " + message + "\nFrom: " + requester;
    }	
}
