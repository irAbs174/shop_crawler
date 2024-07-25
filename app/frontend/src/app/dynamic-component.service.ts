import { Injectable, ComponentFactoryResolver, ViewContainerRef } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DynamicComponentService {

  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }

  loadComponent(viewContainerRef: ViewContainerRef, component: any) {
    viewContainerRef.clear();
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(component);
    viewContainerRef.createComponent(componentFactory);
  }
}
