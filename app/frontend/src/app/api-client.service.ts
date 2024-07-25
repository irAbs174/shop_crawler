import { Injectable } from '@angular/core';
import axios from 'axios';

// Define the type for the phone number payload
interface PhoneNumberPayload {
  phoneNumbers: string[];
}

@Injectable({
  providedIn: 'root'
})
export class PhoneNumberService {

  private apiUrl = 'http://your-django-server-url/api/send-phone-number/'; // Replace with your Django endpoint

  constructor() { }

  // Function to send a POST request with the phone numbers
  async sendPhoneNumbers(phoneNumbers: string[]): Promise<void> {
    const payload: PhoneNumberPayload = {
      phoneNumbers: phoneNumbers,
    };

    console.log('=> => => phoneNumbers:', phoneNumbers);

    try {
      const response = await axios.post(this.apiUrl, payload, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error sending phone numbers:', error);
    }
  }
}



