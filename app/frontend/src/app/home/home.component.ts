import { DynamicComponentService } from '../dynamic-component.service';
import { Component, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { OrdersComponent } from '../orders/orders.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [OrdersComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent implements OnInit {

  @ViewChild('dynamicComponentContainer', { read: ViewContainerRef, static: true })
  dynamicComponentContainer!: ViewContainerRef;

  constructor(
    private DynamicComponentLoad : DynamicComponentService,
  ){}

  home_hidden = false;

  loadCompomemt(component: any){
    this.DynamicComponentLoad.loadComponent(this.dynamicComponentContainer, component);
  }

  ngOnInit(): void {
    setTimeout(()=>{
      this.home_hidden = true;
      // load orders component
      this.loadCompomemt(OrdersComponent);
    }, 1000);
  }

}



