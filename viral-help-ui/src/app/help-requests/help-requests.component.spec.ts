import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HelpRequestsComponent } from './help-requests.component';

describe('HelpRequestsComponent', () => {
  let component: HelpRequestsComponent;
  let fixture: ComponentFixture<HelpRequestsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HelpRequestsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HelpRequestsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
