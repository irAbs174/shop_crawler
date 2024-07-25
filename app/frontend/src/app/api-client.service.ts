import { Injectable } from '@angular/core';
import axios from 'axios';

// Define the type for the phone number payload
interface dataPayload {
  data: string[];
}

@Injectable({
  providedIn: 'root'
})
export class DataSendService {

  private apiUrl = 'http://your-django-server-url/api/send-phone-number/'; // Replace with your Django endpoint

  constructor() { }

  // Function to send a POST request with the phone numbers
  async sendData(data: string): Promise<void> {
    const payload: dataPayload = {
      data: [data],
    };

    console.log('=> => => data:', data);

    try {
      const response = await axios.post(this.apiUrl, payload, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error sending data:', error);
    }
  }
}
