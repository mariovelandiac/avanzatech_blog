import { Component, OnInit } from '@angular/core';
import { PostContentComponent } from '../post-content/post-content.component';
import { Post } from '../../models/interfaces/post.interface';
import { PostService } from '../../services/post.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-post-list',
  standalone: true,
  imports: [PostContentComponent, CommonModule],
  templateUrl: './post-list.component.html',
  styleUrl: './post-list.component.sass'
})
export class PostListComponent implements OnInit {
  posts!: Post[];

  constructor(
    private postService: PostService
  ) {}

  ngOnInit() {
    this.postService.list().subscribe(posts => {
      console.log(posts)
      this.posts = posts;
    });
  }
}
