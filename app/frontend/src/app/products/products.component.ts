import { Component, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import {LoadingService} from '../loading.service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { OrdersComponent } from '../orders/orders.component';
import { DynamicComponentService } from '../dynamic-component.service';

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatGridListModule, OrdersComponent],
  templateUrl: './products.component.html',
  styleUrl: './products.component.css'
})
export class ProductsComponent implements OnInit  {

    @ViewChild('dynamicComponentContainer', { read: ViewContainerRef, static: true })
  dynamicComponentContainer!: ViewContainerRef;

  constructor(
    private loadingService: LoadingService,
    private LoadComponent: DynamicComponentService,
  ){}

    componentLoad(component: any){
    this.LoadComponent.loadComponent(this.dynamicComponentContainer, component);
  }

  products_show = false;

  back(){
    this.products_show = true;
    this.componentLoad(OrdersComponent);
  };

  ngOnInit(): void {
    this.loadingService.simulateLoading()
  };

}

