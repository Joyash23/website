import { Component, OnInit } from '@angular/core';
import { HelpRequest } from '../help-request';

@Component({
  selector: 'app-help-requests',
  templateUrl: './help-requests.component.html',
  styleUrls: ['./help-requests.component.css']
})
export class HelpRequestsComponent implements OnInit {

  helpRequests: HelpRequest[] = [
    { message: 'I need help!', postcode: 8041 },
    { message: 'I also need help!', postcode: 8042 }
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
